import uuid
from fastapi import APIRouter
from services.JWT import JWT
from services.WalletHash import WalletHash
from starlette.responses import JSONResponse
from models.LoginModel import LoginModel
from database.Account import accountDb
from database.AccountToken import accountTokenDb

router = APIRouter()

@router.post("/login", tags=['user'])
async def login(login_model: LoginModel):
    if login_model.wallet_address != None and login_model.encrypted_wallet != None:
        wallet_hash = WalletHash.wallet_hash(login_model.encrypted_wallet)
        user_uuid = accountDb.fetch(wallet_hash)
        if len(user_uuid) == 0:
            new_uuid = uuid.uuid4()
            if accountDb.insert(str(new_uuid), wallet_hash):
                jwt = JWT.signJWT(str(new_uuid))
                accountTokenDb.insert(str(new_uuid), jwt)
                return JSONResponse({"access_token": jwt}, status_code=201)
        else:
            user_uuid = user_uuid[0][0]
            jwt = JWT.signJWT(user_uuid)
            accountTokenDb.update(user_uuid, jwt)
            return JSONResponse({"access_token": jwt})
    else:
        return JSONResponse({"error": "Wallet ID not found"}, status_code=400)