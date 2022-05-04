from fastapi import APIRouter, Depends
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
from starlette.responses import JSONResponse
from services.user import UserService
from models.response.ProfileResponseModel import ProfileResponseModel
from models.input.ProfileModel import ProfileModel

router = APIRouter(prefix='/user')

@router.get('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}})
async def get_profile(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    profile = UserService.get_profile(jwt['uuid'])
    return JSONResponse(profile)

@router.patch('/profile', dependencies=[Depends(JWTChecker())], tags=['user'])
async def update_profile(profile_model: ProfileModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    is_updated = UserService.update_profile(jwt['uuid'], profile_model.username, profile_model.email)
    if is_updated:
        return profile_model
    else:
        return JSONResponse({'error': "Can't update your profile"}, status_code=400)