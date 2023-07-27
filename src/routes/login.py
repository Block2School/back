from fastapi import APIRouter, Request
from models.response.BannedResponseModel import BannedResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.LoginResponseModel import LoginResponseModel
from services.login import LoginService
from starlette.responses import JSONResponse
from models.input.LoginModel import LoginModel
from models.input.RefreshTokenModel import RefreshTokenModel
from services.utils.Log import Log

router = APIRouter()

login_responses = {
    200: {"model": LoginResponseModel},
    201: {"model": LoginResponseModel},
    400: {"model": ErrorResponseModel},
    403: {"model": BannedResponseModel}
}

refresh_responses = {
    200: {"model": LoginResponseModel},
    400: {"model": ErrorResponseModel}
}

@router.post("/login", tags=['user'], responses=login_responses)
async def login(req: Request, login_model: LoginModel):
    Log.route_log(req, "login routes", "open_route")
    if login_model.wallet_address != None and login_model.encrypted_wallet != None:
        response = LoginService.check_account(login_model.encrypted_wallet)
        if len(response) == 1:
            register = LoginService.register(response[0], login_model.wallet_address)
            refresh_token = LoginService.create_refresh_token(register)
            if register != None:
                Log.register_log(req, login_model.wallet_address)
                return JSONResponse({"access_token": register, "token_type": 'Bearer', "refresh_token": refresh_token}, status_code=201)
            else:
                return JSONResponse({"error": "An error occured on account creation"}, status_code=400)
        else:
            if response[2] == None and response[3] == None:
                is_banned = LoginService.is_banned(response[1])
                if is_banned != None:
                    Log.login_log(req, login_model.wallet_address, False, True)
                    return JSONResponse({"error": "User is banned", "reason": is_banned['reason'], "expires": is_banned['expires']}, status_code=403)
                access_token = LoginService.login(response[1])
                refresh_token = LoginService.create_refresh_token(access_token)
                Log.login_log(req, login_model.wallet_address, False)
                return JSONResponse({"access_token": access_token, "token_type": 'Bearer', "refresh_token": refresh_token})
            else:
                if login_model.token != None:
                    access_token = LoginService.login(response[1], login_model.token)
                    if access_token != None:
                        refresh_token = LoginService.create_refresh_token(access_token)
                        Log.login_log(req, login_model.wallet_address, False)
                        return JSONResponse({"access_token": access_token, "token_type": 'Bearer', 'refresh_token': refresh_token})
                    else:
                        Log.login_log(req, login_model.wallet_address)
                        return JSONResponse({"error": "Bad token"}, status_code=403)
                else:
                    Log.login_log(req, login_model.wallet_address)
                    return JSONResponse({"error": "Need a token"}, status_code=403)
    else:
        return JSONResponse({"error": "Invalid body"}, status_code=400)

@router.post('/refresh_token', tags=['user'], responses=refresh_responses)
async def refresh_token(r: Request, refresh_model: RefreshTokenModel):
    Log.route_log(r, "login routes", "open_route")
    if refresh_model.refresh_token != None:
        tokens = LoginService.refresh_token(refresh_model.refresh_token)
        if tokens != None:
            return JSONResponse({"access_token": tokens['access_token'], "token_type": "Bearer", "refresh_token": tokens['refresh_token']})
        else:
            return JSONResponse({"error": "Invalid or expired refresh token"}, status_code=400)
    else:
        return JSONResponse({"error": "Invalid body"}, status_code=400)
