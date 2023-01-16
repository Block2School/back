from fastapi import APIRouter
from models.response.BannedResponseModel import BannedResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.LoginResponseModel import LoginResponseModel
from services.login import LoginService
from starlette.responses import JSONResponse
from models.input.LoginModel import LoginModel

router = APIRouter()

login_responses = {
    200: {"model": LoginResponseModel},
    201: {"model": LoginResponseModel},
    400: {"model": ErrorResponseModel},
    403: {"model": BannedResponseModel}
}

@router.post("/login", tags=['user'], responses=login_responses)
async def login(login_model: LoginModel):
    if login_model.wallet_address != None and login_model.encrypted_wallet != None:
        response = LoginService.check_account(login_model.encrypted_wallet)
        if len(response) == 1:
            register = LoginService.register(response[0], login_model.wallet_address)
            if register != None:
                return JSONResponse({"access_token": register, "token_type": 'Bearer'}, status_code=201)
            else:
                return JSONResponse({"error": "An error occured on account creation"}, status_code=400)
        else:
            if response[2] == None:
                access_token = LoginService.login(response[1])
                is_banned = LoginService.is_banned(response[1])
                if is_banned != None:
                    return JSONResponse({"error": "User is banned", "reason": is_banned['reason'], "expires": is_banned['expires']}, status_code=403)
                return JSONResponse({"access_token": access_token, "token_type": 'Bearer'})
            else:
                if login_model.discord_token != None:
                    access_token = LoginService.login(response[1], login_model.discord_token)
                    if access_token != None:
                        return JSONResponse({"access_token": access_token, "token_type": 'Bearer'})
                    else:
                        return JSONResponse({"error": "Bad discord token"}, status_code=403)
                else:
                    return JSONResponse({"error": "Need a discord token"}, status_code=403)
    else:
        return JSONResponse({"error": "Invalid body"}, status_code=400)