from typing import Optional
from fastapi import APIRouter, Depends, Request
from models.input.SubmitTutorialModel import SubmitTutorialModel
from models.response.CategoryResponseListModel import CategoryResponseListModel
from models.response.CompleteTutorialResponseModel import CompleteTutorialResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.ScoreboardTutorialIDListModel import ScoreboardTutorialIDListModel
from models.response.TutorialResponseListModel import TutorialResponseListModel, TutorialResponseListModelV2
from models.response.TutorialResponseModel import TutorialResponseModel, TutorialResponseModelV2
from models.response.ScoreboardTutorialMeListModel import ScoreboardTutorialMeListModel
from models.response.SuccessByIDModel import SuccessByIDModel
from models.response.SuccessMeModel import SuccessMeModel
from database.Database import Database
from database.UserTutorialScore import UserTutorialScore
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.JWT import JWT
import requests, os, json
from services.utils.Log import Log

from services.utils.JWTChecker import JWTChecker

get_all_tutorials_response = {
    200: {'model': TutorialResponseListModel}
}

get_all_tutorials_responseV2 = {
    200: {'model': TutorialResponseListModelV2}
}

get_tutorial_response = {
    200: {'model': TutorialResponseModel},
    400: {'model': ErrorResponseModel}
}

get_tutorial_responseV2 = {
    200: {'model': TutorialResponseModelV2},
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
async def get_all_tutorials(r: Request) -> JSONResponse:
    """
    Récupérer tous les tutoriaux
    """
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial_list = TutorialService.get_all_tutorials()
    return JSONResponse({'data': tutorial_list}, status_code=200)

@router.get('/v2/auth/all', tags=['tutorial'], responses=get_all_tutorials_responseV2)
async def get_all_tutorialsv2(r: Request, token: str = Depends(JWTChecker())):
    Log.route_log(r, "tutorial routes v2", "open_route")
    jwt = JWT.decodeJWT(token)
    print(jwt)
    tutorial_list = TutorialService.get_all_tutorialsV2(jwt["uuid"])
    return JSONResponse({'data': tutorial_list})

@router.get('/v2/all', tags=['tutorial'], responses=get_all_tutorials_responseV2)
async def get_all_tutorialsv2(r: Request):
    Log.route_log(r, "tutorial routes v2", "open_route")
    tutorial_list = TutorialService.get_all_tutorialsV2("")
    return JSONResponse({'data': tutorial_list})

@router.get('/v2/{id}', tags=['tutorial'], responses=get_tutorial_responseV2)
async def get_tutorialv2(r: Request, id: int):
    Log.route_log(r, "tutorial routes v2", "open_route")
    tutorial = TutorialService.get_tutorialV2(id, "")
    if tutorial == None:
        return JSONResponse({'error': 'Tutorial not found'}, status_code=400)
    else:
        return JSONResponse(tutorial)

@router.get('/v2/auth/{id}', tags=['tutorial'], responses=get_tutorial_responseV2)
async def get_tutorialv2(r: Request, id: int, token: str = Depends(JWTChecker())):
    Log.route_log(r, "tutorial routes v2", "open_route")
    jwt = JWT.decodeJWT(token)
    print(jwt)
    tutorial = TutorialService.get_tutorialV2(id, jwt["uuid"])
    if tutorial == None:
        return JSONResponse({'error': 'Tutorial not found'}, status_code=400)
    else:
        return JSONResponse(tutorial)

@router.get('/{id}', tags=['tutorial'], responses=get_tutorial_response)
async def get_tutorial(r: Request, id: int) -> JSONResponse:
    """
    Récupérer un tutoriel par son ID
    """
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial = TutorialService.get_tutorial(id)
    if tutorial == None:
        return JSONResponse({'error': 'Tutorial not found'}, status_code=400)
    else:
        return JSONResponse(tutorial, status_code=200)

@router.get('/category/all', tags=['tutorial'], responses=get_category_list_response)
async def get_all_categories(r: Request) -> JSONResponse:
    """
    Récupérer toutes les catégories
    """
    Log.route_log(r, "tutorial routes", "open_route")
    categories = TutorialService.get_all_categories()
    return JSONResponse({'data': categories}, status_code=200)

@router.get('/category/{category}', tags=['tutorial'], responses=get_all_tutorials_by_category_response)
async def get_all_tutorials_by_category(r: Request, category: str) -> JSONResponse:
    """
    Récupérer tous les tutoriaux par catégorie
    """
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial_list = TutorialService.get_all_tutorials_by_category(category)
    return JSONResponse({'data': tutorial_list}, status_code=200)

@router.get('/scoreboard/id/{id}', tags=['tutorial'], responses=get_scoreboard_tutorial_response)
async def get_scoreboard_tutorial(r: Request, id: int) -> JSONResponse:
    """
    Récupérer le scoreboard du tutoriel par son ID
    """
    Log.route_log(r, "tutorial routes", "open_route")
    scoreboard_tutorial = TutorialService.get_scoreboard_tutorial_id(id)
    return JSONResponse({'data': scoreboard_tutorial}, status_code=200)

@router.get('/success/id/{id}', tags=['tutorial'], responses=get_success_by_id)
async def get_success_percentage_tutorial(r: Request, id: int) -> JSONResponse:
    """
    Récupérer le pourcentage de complétion du tutoriel par son ID
    """
    Log.route_log(r, "tutorial routes", "open_route")
    percentage = TutorialService.get_percentage_tutorial_id(id)

    return JSONResponse({'percentage': percentage}, status_code=200)

@router.get('/scoreboard/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_scoreboard_me_tutorial_response)
async def get_user_all_score(r: Request, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupérer tous les score de l'utilisateur connecté
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])
    scoreboard = TutorialService.get_user_scoreboard(jwt['uuid'])

    return JSONResponse({'data': scoreboard}, status_code=200)

@router.get('/success/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_success_me_response)
async def get_user_success_tutorials(r: Request, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupérer le nombre de tutoriaux total complétés de l'utilisateur
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])
    success = TutorialService.get_user_success(jwt['uuid'])
    nb_tutorials = TutorialService.get_total_number_tutorials()

    return JSONResponse({'data': success, 'total_completion': (len(success) / nb_tutorials) * 100}, status_code=200)

@router.post('/complete', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=submit_tutorial_responses)
async def complete_tutorial(r: Request, tutorial: SubmitTutorialModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Compléter un tutoriel
    """
    userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])

    check = False
    available_language = ['js','py','R','cpp', 'c', 'solidity']
    if (tutorial.language not in available_language):
        return JSONResponse({'error': 'Unsupported language'}, status_code=400)

    if tutorial.source_code != None:
        tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
        
        if (tutorial.exec == True):
            data = {
                "code": tutorial.source_code,
                "language": tutorial.language,
                "input": tuto['inputs'],
                "id": tutorial.tutorial_id,
            }
            data = json.dumps(data)
            # {'code': "const helloWorld = () => {\n    console.log('hello world');\n};", 'language': 'js'}
            r = requests.post(os.getenv('CODE_EXEC_URL') + '/execute', data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                })
            r.raise_for_status()
            if r.status_code == 200:
                r = r.json()
            # tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
            # tuto['answer'] += '\n'
            if tuto['answer'] == r['output']:
                check = True
            # check = False
        else:
            check = False
            tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
        if (tuto != None and (check == True or tuto['answer'] == tutorial.source_code)):
            result = TutorialService.validate_tutorial(jwt['uuid'], tutorial.tutorial_id, tutorial.language, tutorial.characters, tutorial.lines)
            # FETCH si None insert otherwise update
            fetch = userTutorialScoreDb.fetch(jwt['uuid'], tutorial.tutorial_id, tutorial.language)
            lang_diff = userTutorialScoreDb.fetch_all_score_of_user_by_tutorial_id(jwt['uuid'], tutorial.tutorial_id)
            langlist = []
            for i in range(len(lang_diff)):
                langlist.append(lang_diff[i]['language'])
            if (fetch == None): # ou tuto pas validé dans le language ?
                userTutorialScoreDb.insert(jwt['uuid'], tutorial.tutorial_id, tutorial.language, tutorial.characters, tutorial.lines)
            else:
                if (tutorial.characters < fetch['characters'] and tutorial.lines < fetch['lines']):
                    userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, tutorial.characters, tutorial.lines)
                elif (tutorial.characters < fetch['characters'] and tutorial.lines >= fetch['lines']):
                    userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, tutorial.characters, -1)
                elif (tutorial.characters >= fetch['characters'] and tutorial.lines < fetch['lines']):
                    userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, -1, tutorial.lines)
            userTutorialScoreDb.close()
            return JSONResponse({'is_correct': True, 'total_completions': result, 'error': None, "received": r['output']})
        else:
            return JSONResponse({'is_correct': False, 'total_completions': 0, 'error': r['error'], "received": r['output']})
    else:
        return JSONResponse({'error': 'Missing source code or language'}, status_code=400)
