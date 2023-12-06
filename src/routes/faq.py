from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from services.faq import FaqService
from models.response.FaqListResponseModel import FaqListResponseModel
from services.utils.Log import Log

router = APIRouter(prefix='/faq')

@router.get('/all', tags=['faq'], responses={200: {"model": FaqListResponseModel}})
async def get_all_faq(r: Request) -> JSONResponse:
    """
    Récupération de la FAQ
    """
    Log.route_log(r, "FAQ", "open_route")
    response = FaqService.get_all_faq()
    return JSONResponse(response, status_code=200)