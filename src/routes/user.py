from fastapi import APIRouter, Depends, Request
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
from starlette.responses import JSONResponse
from services.user import UserService
from models.response.ProfileResponseModel import ProfileResponseModel
from models.input.ProfileModel import ProfileModel
from models.input.NeedWordlistModel import NeedWordListModel
from models.response.SuccessResponseModel import SuccessResponseModel
from models.response.FriendsListResponseModel import FriendsListResponseModel
from models.input.FriendsModel import FriendsModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.input.WordlistModel import WordlistModel
from models.response.QrCodeResponseModel import QrCodeResponseModel
from services.utils.Log import Log

router = APIRouter(prefix='/user')

@router.get('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}})
async def get_profile(r: Request, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupérer le profil de l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    profile = UserService.get_profile(jwt['uuid'])
    return JSONResponse(profile, status_code=200)

@router.patch('/profile', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileModel}})
async def update_profile(r: Request, profile_model: ProfileModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Modifier le profil de l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    is_updated = UserService.update_profile(jwt['uuid'], profile_model.username, profile_model.email, profile_model.description, profile_model.twitter, profile_model.youtube, profile_model.birthdate, profile_model.privacy)
    if is_updated:
        return JSONResponse(profile_model, status_code=200)
    else:
        return JSONResponse({'error': "Can't update your profile"}, status_code=400)

@router.get('/profile/{username}', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": ProfileResponseModel}, 401: {"model": ErrorResponseModel}})
async def get_user_profile(r: Request, username: str, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupérer le profil d'un utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    response = UserService.get_user_privacy(jwt['uuid'], username)
    if response != None:
        return JSONResponse(response, status_code=200)
    else:
        return JSONResponse({"error": "You're not allowed to see this profile"}, status_code=401)

@router.post('/authenticator/qrcode', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": QrCodeResponseModel}, 400: {"model": ErrorResponseModel}})
async def add_qrcode_authenticator(r: Request, wordlist_model: WordlistModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Activer la double authentification TOTP
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if wordlist_model.wordlist == None:
        wordlist = UserService.activate_authenticator(jwt['uuid'])
        if wordlist == None:
            return JSONResponse({"error": "You need to specify the wordlist to activate the 2FA TOTP Authentication"}, status_code=400)
    else:
        wordlist = wordlist_model.wordlist
    qr_code = UserService.add_totp(jwt['uuid'], wordlist)
    if qr_code:
        return JSONResponse({"qr": qr_code, "wordlist": wordlist if wordlist_model.wordlist == None else None}, status_code=200)
    else:
        return JSONResponse({"error": "Can't activate TOTP Authenticator"}, status_code=400)

@router.delete('/authenticator/qrcode', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def remove_qrcode_authenticator(r: Request, wordlist_model: WordlistModel, credentials: str= Depends(JWTChecker())) -> JSONResponse:
    """
    Supprimer la double authentification TOTP
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if wordlist_model.wordlist == None:
        return JSONResponse({"error": "Need a wordlist to remove TOTP Authenticator"}, status_code=400)
    result = UserService.remove_totp(jwt['uuid'], wordlist_model.wordlist)
    if result:
        return JSONResponse({"success": "Removed TOTP Authenticator"}, status_code=200)
    else:
        return JSONResponse({"error": "Wordlist is invalid or TOTP Authenticator is not enabled"}, status_code=400)

@router.delete('/authenticator/discord', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def remove_discord_authenticator(r: Request, wordlist_model: NeedWordListModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    @deprecated

    Supprimer la double authentification Discord
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if wordlist_model.wordlist != None:
        is_ok = UserService.remove_discord_tag(jwt['uuid'], wordlist_model.wordlist)
        if is_ok:
            return JSONResponse({"success": "Removed discord tag"}, status_code=200)
        else:
            return JSONResponse({"error": "Bad wordlist or no discord tag found"}, status_code=400)
    else:
        return JSONResponse({"error": "Need a wordlist"}, status_code=400)

@router.get('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": FriendsListResponseModel}})
async def get_friends(r: Request, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupérer la liste d'amis de l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    friends = UserService.get_friend_list(jwt['uuid'])
    if friends != None:
        return JSONResponse({"data": friends}, status_code=200)
    return JSONResponse({"data": []}, status_code=200)

@router.post('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def add_friend(r: Request, friend: FriendsModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Ajouter un nouvel ami pour l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if friend.friend_uuid != None:
        result = UserService.add_friend(jwt['uuid'], friend.friend_uuid)
        if result == "pending":
            return JSONResponse({"success": "Friend request is pending"}, status_code=200)
        elif result == "friend":
            return JSONResponse({"success": "Now friends with"}, status_code=200)
        else:
            return JSONResponse({"error": "You are already friend with or pending invite"}, status_code=201)
    else:
        return JSONResponse({"error": "You must provid a friend uuid"}, status_code=400)

@router.delete('/friends', dependencies=[Depends(JWTChecker())], tags=['user'], responses={200: {"model": SuccessResponseModel}, 400: {"model": ErrorResponseModel}})
async def remove_friend(r: Request, friend: FriendsModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Supprimer un ami de l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if friend.friend_uuid != None:
        result = UserService.remove_friend(jwt['uuid'], friend.friend_uuid)
        if result:
            return JSONResponse({"success": "Friend removed"}, status_code=200)
        else:
            return JSONResponse({"error": "You're not friends"}, status_code=400)
    else:
        return JSONResponse({"error": "You must provide a friend uuid"}, status_code=400)

@router.get("/search", dependencies=[Depends(JWTChecker())], tags=["user"])
async def search_user(r: Request, user: str = None, page: int = 1, offset: int = 50, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Rechercher un utilisateur par son nom
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "user routes", jwt["uuid"])
    if not user:
        return JSONResponse({"error": "You must provide a partial username"}, status_code=400)
    response = UserService.search_user(user, page, offset)
    if not response:
        return JSONResponse({"error": "Invalid parameters"}, status_code=400)
    return JSONResponse(response, status_code=200)