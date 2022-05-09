from fastapi import APIRouter
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.LoginResponseModel import LoginResponseModel
from services.login import LoginService
from starlette.responses import JSONResponse
from models.input.LoginModel import LoginModel

router = APIRouter()

login_responses = {
    200: {"model": LoginResponseModel},
    201: {"model": LoginResponseModel},
    400: {"model": ErrorResponseModel}
}

@router.post("/login", tags=['user'], responses=login_responses)
async def login(login_model: LoginModel):
    if login_model.wallet_address != None and login_model.encrypted_wallet != None:
        response = LoginService.check_account(login_model.encrypted_wallet)
        if len(response) == 1:
            register = LoginService.register(response[0], login_model.wallet_address)
            if register != None:
                return JSONResponse({"access_token": register, "token_type": 'Bearer'})
            else:
                return JSONResponse({"error": "An error occured on account creation"}, status_code=400)
        else:
            return JSONResponse({"access_token": LoginService.login(response[1])})
    else:
        return JSONResponse({"error": "Invalid body"}, status_code=400)