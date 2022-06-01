from fastapi import APIRouter, Depends
from models.response.CategoryResponseListModel import CategoryResponseListModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.TutorialResponseListModel import TutorialResponseListModel
from models.response.TutorialResponseModel import TutorialResponseModel
from services.tutorial import TutorialService
from starlette.responses import JSONResponse

from services.utils.JWTChecker import JWTChecker

get_all_tutorials_response = {
    200: {'model': TutorialResponseListModel}
}
get_tutorial_response = {
    200: {'model': TutorialResponseModel},
    400: {'model': ErrorResponseModel}
}
get_all_tutorials_by_category_response = {
    200: {'model': TutorialResponseListModel}
}

get_category_list_response = {
    200: {'model': CategoryResponseListModel}
}

router = APIRouter(prefix='/tuto')

@router.get('/all', tags=['tutorial'], responses=get_all_tutorials_response)
async def get_all_tutorials():
    tutorial_list = TutorialService.get_all_tutorials()
    return JSONResponse({'data': tutorial_list})

@router.get('/{id}', tags=['tutorial'], responses=get_tutorial_response)
async def get_tutorial(id: int):
    tutorial = TutorialService.get_tutorial(id)
    if tutorial == None:
        return JSONResponse({'error': 'Tutorial not found'}, status_code=400)
    else:
        return JSONResponse(tutorial)

@router.get('/category/all', tags=['tutorial'], responses=get_category_list_response)
async def get_all_categories():
    categories = TutorialService.get_all_categories()
    return JSONResponse({'data': categories})

@router.get('/category/{category}', tags=['tutorial'], responses=get_all_tutorials_by_category_response)
async def get_all_tutorials_by_category(category: str):
    tutorial_list = TutorialService.get_all_tutorials_by_category(category)
    return JSONResponse({'data': tutorial_list})

@router.get('/scoreboard/{id}', tags=['tutorial'])
async def get_scoreboard_tutorial(id: int):
    pass

@router.get('/success/{id}', tags=['tutorial'])
async def get_success_percentage_tutorial(id: int):
    pass

@router.get('/scoreboard/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())])
async def get_user_all_score(credentials: str = Depends(JWTChecker())):
    pass

@router.get('/scoreboard/me/{id}', tags=['tutorial'], dependencies=[Depends(JWTChecker())])
async def get_user_score_tutorial(id: int, credentials: str = Depends(JWTChecker())):
    pass

@router.get('/success/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())])
async def get_user_success_tutorials(credentials: str = Depends(JWTChecker())):
    pass

@router.post('/complete', tags=['tutorial'], dependencies=[Depends(JWTChecker())])
async def complete_tutorial(credentials: str = Depends(JWTChecker())):
    pass