from fastapi import APIRouter, Depends
from models.input.SubmitTutorialModel import SubmitTutorialModel
from models.response.CategoryResponseListModel import CategoryResponseListModel
from models.response.CompleteTutorialResponseModel import CompleteTutorialResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.TutorialResponseListModel import TutorialResponseListModel
from models.response.TutorialResponseModel import TutorialResponseModel
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.JWT import JWT

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

submit_tutorial_responses = {
    200: {'model': CompleteTutorialResponseModel},
    400: {'model': ErrorResponseModel}
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

@router.post('/complete', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=submit_tutorial_responses)
async def complete_tutorial(tutorial: SubmitTutorialModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)

    if tutorial.is_already_checked:
        result = TutorialService.validate_tutorial(jwt['uuid'], tutorial.tutorial_id)
        return JSONResponse({'is_correct': True, 'total_completions': result, 'error_description': None})
    else:
        if tutorial.source_code != None and tutorial.language != None:
            pass # TO DO
            return JSONResponse({'is_correct': False, 'total_completions': 0, 'error_description': 'Not implemented'})
        else:
            return JSONResponse({'error': 'Missing source code or language'}, status_code=400)
