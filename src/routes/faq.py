from fastapi import APIRouter, Depends
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
from starlette.responses import JSONResponse
from services.user import FaqService
from models.response.ProfileResponseModel import ProfileResponseModel
from models.input.ProfileModel import ProfileModel
from models.response.AddDiscordAuthenticatorResponseModel import AddDiscordAuthenticatorResponseModel
from models.input.AddDiscordAuthenticatorModel import AddDiscordAuthenticatorModel
from models.input.NeedWordlistModel import NeedWordListModel
from models.response.SuccessResponseModel import SuccessResponseModel
from models.response.FaqListResponseModel import FaqListResponseModel

router = APIRouter(prefix='/faq')

@router.get('/all', tags=['faq'], responses={200: {"model": FaqListResponseModel}})
async def get_all_faq():
    response = FaqService.get_all_faq()
    return JSONResponse(response)