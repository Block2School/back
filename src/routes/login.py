from fastapi import APIRouter
from starlette.responses import JSONResponse
from models.LoginModel import LoginModel

router = APIRouter()

@router.post("/login", tags=['user'])
async def login(login_model: LoginModel):
  if login_model.wallet_address != None:
    pass
    # return JWT token
  else:
    JSONResponse({"error": "Wallet ID not found"}, status_code=401)