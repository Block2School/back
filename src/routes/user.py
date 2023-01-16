from fastapi import APIRouter, Depends
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
from starlette.responses import JSONResponse
from services.user import UserService
from models.response.ProfileResponseModel import ProfileResponseModel
from models.input.ProfileModel import ProfileModel
from models.response.AddDiscordAuthenticatorResponseModel import AddDiscordAuthenticatorResponseModel
from models.input.AddDiscordAuthenticatorModel import AddDiscordAuthenticatorModel
from models.input.NeedWordlistModel import NeedWordListModel
from models.response.RemovedAuthenticatorResponseModel import RemovedAuthenticatorResponseModel

router = APIRouter(prefix='/user')

@router.get('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}})
async def get_profile(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    profile = UserService.get_profile(jwt['uuid'])
    return JSONResponse(profile)

@router.patch('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileModel}})
async def update_profile(profile_model: ProfileModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    is_updated = UserService.update_profile(jwt['uuid'], profile_model.username, profile_model.email, profile_model.description, profile_model.twitter, profile_model.youtube, profile_model.birthdate)
    if is_updated:
        return profile_model
    else:
        return JSONResponse({'error': "Can't update your profile"}, status_code=400)

@router.post('/authenticator/discord', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": AddDiscordAuthenticatorResponseModel}})
async def add_discord_authenticator(discord_authenticator_model: AddDiscordAuthenticatorModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if discord_authenticator_model.discord_tag != None:
        wordlist = UserService.activate_authenticator(jwt['uuid'])
        is_ok = UserService.add_discord_tag(jwt['uuid'], discord_authenticator_model.discord_tag, discord_authenticator_model.wordlist if wordlist == None else wordlist)
        if is_ok:
            return JSONResponse({"wordlist": wordlist})
        else:
            return JSONResponse({"error": "Need a good wordlist or discord tag already linked"}, status_code=400)
    else:
        return JSONResponse({"error": "Need a discord tag"}, status_code=400)

@router.delete('/authenticator/discord', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": RemovedAuthenticatorResponseModel}})
async def remove_discord_authenticator(wordlist_model: NeedWordListModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if wordlist_model.wordlist != None:
        is_ok = UserService.remove_discord_tag(jwt['uuid'], wordlist_model.wordlist)
        if is_ok:
            return JSONResponse({"success": "Removed discord tag"})
        else:
            return JSONResponse({"error": "Bad wordlist or no discord tag found"}, status_code=400)
    else:
        return JSONResponse({"error": "Need a wordlist"}, status_code=400)