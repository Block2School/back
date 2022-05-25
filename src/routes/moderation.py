from fastapi import APIRouter, Depends
from models.input.BanModel import BanModel
from models.input.ModModel import ModModel
from models.input.TutorialModel import TutorialModel
from models.input.UnbanModel import UnbanModel
from models.response.BanResponseModel import BanResponseModel
from models.response.DataListReponseModel import DataListResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.SuccessResponseModel import SuccessResponseModel
from models.response.UnbanResponseModel import UnbanResponseModel
from services.moderation import ModerationService
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.AdminChecker import AdminChecker
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker

router = APIRouter(prefix='/admin')

banlist_responses = {
    200: {'model': DataListResponseModel},
    400: {'model': ErrorResponseModel}
}
ban_responses = {
    200: {'model': BanResponseModel},
    400: {'model': ErrorResponseModel}
}
unban_responses = {
    200: {'model': UnbanResponseModel},
    400: {'model': ErrorResponseModel}
}
set_mod_responses = {
    200: {'model': ModModel},
    400: {'model': ErrorResponseModel}
}
create_tutorial_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}

@router.get('/banlist/{uuid}', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=banlist_responses)
async def get_banlist(uuid: str):
    datas = ModerationService.get_banlist(uuid)
    return JSONResponse({"data": datas})

@router.post('/ban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=ban_responses)
async def ban(ban_model: BanModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if ban_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_banned = ModerationService.ban(ban_model.uuid, jwt['uuid'], ban_model.reason, ban_model.expires)
        if is_banned:
            return JSONResponse({"uuid": ban_model.uuid, "banned_by": jwt['uuid'], "reason": ban_model.reason, "expires": ban_model.expires})
        else:
            return JSONResponse({"error": "Cannot ban this user"}, status_code=400)

@router.post('/unban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=unban_responses)
async def unban(revoke: UnbanModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if revoke.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_unbanned = ModerationService.unban(revoke.uuid, jwt['uuid'], revoke.reason)
        if is_unbanned:
            return JSONResponse({"uuid": revoke.uuid, "revoked_by": jwt['uuid'], "reason": revoke.reason})
        else:
            return JSONResponse({"error": "Cannot unban this user"}, status_code=400)

@router.post('/mod', dependencies=[Depends(AdminChecker(2))], tags=['admin'])
async def set_mod(mod_model: ModModel):
    if mod_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_changed = ModerationService.set_mod(mod_model.uuid, mod_model.role)
        if is_changed:
            return JSONResponse({"uuid": mod_model.uuid, "role": mod_model.role})
        else:
            return JSONResponse({"error": "Cannot change mod role of this user"}, status_code=400)

@router.post('/tuto/create', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=create_tutorial_responses)
async def create_tutorial(tutorial_model: TutorialModel):
    if tutorial_model.answer == None:
        return JSONResponse({'error': 'Unknown answer'}, status_code=400)
    elif tutorial_model.category == None:
        return JSONResponse({'error': 'Unknown category'}, status_code=400)
    elif tutorial_model.markdownUrl == None:
        return JSONResponse({'error': 'Unknown markdown URL'}, status_code=400)
    elif tutorial_model.title == None:
        return JSONResponse({'error': 'Unknown title'}, status_code=400)
    elif tutorial_model.startCode == None:
        return JSONResponse({'error': 'Unknown start code'}, status_code=400)
    elif tutorial_model.shouldBeCheck == None:
        return JSONResponse({'error': 'Unknown should be check boolean'}, status_code=400)
    result = TutorialService.create_tutorial(tutorial_model.title, tutorial_model.markdownUrl, tutorial_model.startCode, tutorial_model.category, tutorial_model.answer, tutorial_model.shouldBeCheck)
    if result:
        return JSONResponse({"success": "Tutorial created !"})
    else:
        return JSONResponse({"error": "This tutorial already exists"}, status_code=400)
