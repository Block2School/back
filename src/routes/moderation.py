from fastapi import APIRouter, Depends
from models.response.DataListReponseModel import DataListResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from services.moderation import ModerationService
from starlette.responses import JSONResponse
from services.utils.AdminChecker import AdminChecker

router = APIRouter(prefix='/admin')

banlist_responses = {
    200: {'model': DataListResponseModel},
    400: {'model': ErrorResponseModel}
}

@router.get('/banlist/{uuid}', dependencies=[Depends(AdminChecker(2))], tags=['moderation'], responses=banlist_responses)
async def get_banlist(uuid: str):
    datas = ModerationService.get_banlist(uuid)
    if len(datas) == 0:
        return JSONResponse({"data": datas}, status_code=204)
    return JSONResponse({"data": datas})