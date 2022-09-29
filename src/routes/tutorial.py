from fastapi import APIRouter, Depends
from models.input.SubmitTutorialModel import SubmitTutorialModel
from models.response.CategoryResponseListModel import CategoryResponseListModel
from models.response.CompleteTutorialResponseModel import CompleteTutorialResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.ScoreboardTutorialIDListModel import ScoreboardTutorialIDListModel
from models.response.TutorialResponseListModel import TutorialResponseListModel
from models.response.TutorialResponseModel import TutorialResponseModel
from models.response.ScoreboardTutorialMeListModel import ScoreboardTutorialMeListModel
from models.response.SuccessByIDModel import SuccessByIDModel
from models.response.SuccessMeModel import SuccessMeModel
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.JWT import JWT
import requests, os, json

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

get_scoreboard_tutorial_response = {
    200: {'model': ScoreboardTutorialIDListModel}
}

get_scoreboard_me_tutorial_response = {
    200: {'model': ScoreboardTutorialMeListModel}
}

get_success_by_id = {
    200: {'model': SuccessByIDModel}
}

get_success_me_response = {
    200: {'model': SuccessMeModel}
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

@router.get('/scoreboard/id/{id}', tags=['tutorial'], responses=get_scoreboard_tutorial_response)
async def get_scoreboard_tutorial(id: int):
    scoreboard_tutorial = TutorialService.get_scoreboard_tutorial_id(id)
    return JSONResponse({'data': scoreboard_tutorial})

@router.get('/success/id/{id}', tags=['tutorial'], responses=get_success_by_id)
async def get_success_percentage_tutorial(id: int):
    percentage = TutorialService.get_percentage_tutorial_id(id)

    return JSONResponse({'percentage': percentage})

@router.get('/scoreboard/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_scoreboard_me_tutorial_response)
async def get_user_all_score(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    scoreboard = TutorialService.get_user_scoreboard(jwt['uuid'])

    return JSONResponse({'data': scoreboard})

@router.get('/success/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_success_me_response)
async def get_user_success_tutorials(credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    success = TutorialService.get_user_success(jwt['uuid'])
    nb_tutorials = TutorialService.get_total_number_tutorials()

    return JSONResponse({'data': success, 'total_completion': (len(success) / nb_tutorials) * 100})

@router.post('/complete', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=submit_tutorial_responses)
async def complete_tutorial(tutorial: SubmitTutorialModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)

    available_language = ['js']
    if (tutorial.language not in available_language):
        return JSONResponse({'error': 'Unsupported language'}, status_code=400)

    if tutorial.is_already_checked:
        print('is_already_checked')
        result = TutorialService.validate_tutorial(jwt['uuid'], tutorial.tutorial_id)
        return JSONResponse({'is_correct': True, 'total_completions': result, 'error_description': None})
    else:
        if tutorial.source_code != None and tutorial.language != None:
            # pass # TO DO
            print(os.getenv('CODE_EXEC_URL') + '/execute')
            data = {
                "code": tutorial.source_code,
                "language": tutorial.language
            }
            data = json.dumps(data)
            print(data) 
            # {'code': "const helloWorld = () => {\n    console.log('hello world');\n};", 'language': 'js'}
            r = requests.post(os.getenv('CODE_EXEC_URL') + '/execute', data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                })
            r.raise_for_status()  # raises exception when not a 2xx r
            if r.status_code == 200:
                r = r.json()
                print('r => ', r['output'])
            # return JSONResponse({'is_correct': False, 'total_completions': 0, 'error_description': 'Not implemented'})
            tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
            print(f'answer == |{tuto["answer"]}| && output == |{r["output"]}| tutorialid == {tutorial.tutorial_id}')
            if (tuto != None and tuto['answer'] == r['output']):
                result = TutorialService.validate_tutorial(jwt['uuid'], tutorial.tutorial_id)
                return JSONResponse({'is_correct': True, 'total_completions': result, 'error_description': None})
            else:
                return JSONResponse({'is_correct': False, 'total_completions': 0, 'error_description': None})

        else:
            return JSONResponse({'error': 'Missing source code or language'}, status_code=400)
