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
from models.response.SuccessResponseModel import SuccessResponseModel
from models.response.FriendsListResponseModel import FriendsListResponseModel
from models.input.FriendsModel import FriendsModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.input.WordlistModel import WordlistModel
from models.response.QrCodeResponseModel import QrCodeResponseModel

router = APIRouter(prefix='/user')

@router.get('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}})
async def get_profile(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    profile = UserService.get_profile(jwt['uuid'])
    return JSONResponse(profile)

@router.patch('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileModel}})
async def update_profile(profile_model: ProfileModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    is_updated = UserService.update_profile(jwt['uuid'], profile_model.username, profile_model.email, profile_model.description, profile_model.twitter, profile_model.youtube, profile_model.birthdate, profile_model.privacy)
    if is_updated:
        return profile_model
    else:
        return JSONResponse({'error': "Can't update your profile"}, status_code=400)

@router.get('/profile/{username}', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}, 401: {"model": ErrorResponseModel}})
async def get_user_profile(username: str, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    response = UserService.get_user_privacy(jwt['uuid'], username)
    if response != None:
        return JSONResponse(response)
    else:
        return JSONResponse({"error": "You're not allowed to see this profile"}, status_code=401)

@router.post('/authenticator/qrcode', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": QrCodeResponseModel}, 400: {"model": ErrorResponseModel}})
async def add_qrcode_authenticator(wordlist_model: WordlistModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if wordlist_model.wordlist == None:
        wordlist = UserService.activate_authenticator(jwt['uuid'])
        if wordlist == None:
            return JSONResponse({"error": "You need to specify the wordlist to activate the 2FA TOTP Authentication"})
    else:
        wordlist = wordlist_model.wordlist
    qr_code = UserService.add_totp(jwt['uuid'], wordlist)
    if qr_code:
        return JSONResponse({"qr": qr_code, "wordlist": wordlist if wordlist_model.wordlist == None else None})
    else:
        return JSONResponse({"error": "Can't activate TOTP Authenticator"}, status_code=400)

@router.delete('/authenticator/qrcode', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def remove_qrcode_authenticator(wordlist_model: WordlistModel, credentials: str= Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if wordlist_model.wordlist == None:
        return JSONResponse({"error": "Need a wordlist to remove TOTP Authenticator"}, status_code=400)
    result = UserService.remove_totp(jwt['uuid'], wordlist_model.wordlist)
    if result:
        return JSONResponse({"success": "Removed TOTP Authenticator"})
    else:
        return JSONResponse({"error": "Wordlist is invalid or TOTP Authenticator is not enabled"}, status_code=400)

@router.post('/authenticator/discord', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": AddDiscordAuthenticatorResponseModel}})
async def add_discord_authenticator(discord_authenticator_model: AddDiscordAuthenticatorModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if discord_authenticator_model.discord_tag != None:
        wordlist = UserService.activate_authenticator(jwt['uuid'])
        is_ok = UserService.add_discord_tag(jwt['uuid'], discord_authenticator_model.discord_tag, discord_authenticator_model.wordlist if wordlist == None else wordlist)
        if is_ok:
            return JSONResponse({"wordlist": wordlist})
        else:
            return JSONResponse({"error": "Need a good wordlist or an authenticator is already enabled"}, status_code=400)
    else:
        return JSONResponse({"error": "Need a discord tag"}, status_code=400)

@router.delete('/authenticator/discord', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
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

@router.get('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": FriendsListResponseModel}})
async def get_friends(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    friends = UserService.get_friend_list(jwt['uuid'])
    if friends != None:
        return JSONResponse({"data": friends})
    return JSONResponse({"data": []})

@router.post('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def add_friend(friend: FriendsModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if friend.friend_uuid != None:
        result = UserService.add_friend(jwt['uuid'], friend.friend_uuid)
        if result == "pending":
            return JSONResponse({"success": "Friend request is pending"})
        elif result == "friend":
            return JSONResponse({"success": "Now friends with"})
        else:
            return JSONResponse({"error": "You are already friend with or pending invite"}, status_code=201)
    else:
        return JSONResponse({"error": "You must provid a friend uuid"}, status_code=400)

@router.delete('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def remove_friend(friend: FriendsModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if friend.friend_uuid != None:
        result = UserService.remove_friend(jwt['uuid'], friend.friend_uuid)
        if result:
            return JSONResponse({"success": "Friend removed"})
        else:
            return JSONResponse({"error": "You're not friends"}, status_code=400)
    else:
        return JSONResponse({"error": "You must provide a friend uuid"}, status_code=400)

@router.get("/search")
async def search_user(user: str = None, page: int = 1, offset: int = 50, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if not user:
        return JSONResponse({"error": "You must provide a partial username"}, status_code=400)
    response = UserService.search_user(user, page, offset)
    if not response:
        return JSONResponse({"error": "Invalid parameters"}, status_code=400)
    return JSONResponse(response)