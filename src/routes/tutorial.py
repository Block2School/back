from fastapi import APIRouter, Depends, Request
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
async def get_all_tutorials(r: Request):
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial_list = TutorialService.get_all_tutorials()
    return JSONResponse({'data': tutorial_list})

@router.get('/{id}', tags=['tutorial'], responses=get_tutorial_response)
async def get_tutorial(r: Request, id: int):
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial = TutorialService.get_tutorial(id)
    if tutorial == None:
        return JSONResponse({'error': 'Tutorial not found'}, status_code=400)
    else:
        return JSONResponse(tutorial)

@router.get('/category/all', tags=['tutorial'], responses=get_category_list_response)
async def get_all_categories(r: Request):
    Log.route_log(r, "tutorial routes", "open_route")
    categories = TutorialService.get_all_categories()
    return JSONResponse({'data': categories})

@router.get('/category/{category}', tags=['tutorial'], responses=get_all_tutorials_by_category_response)
async def get_all_tutorials_by_category(r: Request, category: str):
    Log.route_log(r, "tutorial routes", "open_route")
    tutorial_list = TutorialService.get_all_tutorials_by_category(category)
    return JSONResponse({'data': tutorial_list})

@router.get('/scoreboard/id/{id}', tags=['tutorial'], responses=get_scoreboard_tutorial_response)
async def get_scoreboard_tutorial(r: Request, id: int):
    Log.route_log(r, "tutorial routes", "open_route")
    scoreboard_tutorial = TutorialService.get_scoreboard_tutorial_id(id)
    return JSONResponse({'data': scoreboard_tutorial})

@router.get('/success/id/{id}', tags=['tutorial'], responses=get_success_by_id)
async def get_success_percentage_tutorial(r: Request, id: int):
    Log.route_log(r, "tutorial routes", "open_route")
    percentage = TutorialService.get_percentage_tutorial_id(id)

    return JSONResponse({'percentage': percentage})

@router.get('/scoreboard/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_scoreboard_me_tutorial_response)
async def get_user_all_score(r: Request, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])
    scoreboard = TutorialService.get_user_scoreboard(jwt['uuid'])

    return JSONResponse({'data': scoreboard})

@router.get('/success/me', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=get_success_me_response)
async def get_user_success_tutorials(r: Request, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])
    success = TutorialService.get_user_success(jwt['uuid'])
    nb_tutorials = TutorialService.get_total_number_tutorials()

    return JSONResponse({'data': success, 'total_completion': (len(success) / nb_tutorials) * 100})

@router.post('/complete', tags=['tutorial'], dependencies=[Depends(JWTChecker())], responses=submit_tutorial_responses)
async def complete_tutorial(r: Request, tutorial: SubmitTutorialModel, credentials: str = Depends(JWTChecker())):
    userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "tutorial routes", jwt["uuid"])

    check = False
    available_language = ['js','py','R','cpp', 'c', 'solidity']
    if (tutorial.language not in available_language):
        return JSONResponse({'error': 'Unsupported language'}, status_code=400)

    print(tutorial.source_code + " || " + tutorial.language)
    if tutorial.source_code != None:
        tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
        print('exec => ', tutorial.exec)
        print('tuto.inputs => "', tuto['inputs'], '"')
        
        if (tutorial.exec == True):
            print(os.getenv('CODE_EXEC_URL') + '/execute')
            data = {
                "code": tutorial.source_code,
                "language": tutorial.language,
                "input": tuto['inputs'],
            }
            data = json.dumps(data)
            print(data)
            # {'code': "const helloWorld = () => {\n    console.log('hello world');\n};", 'language': 'js'}
            r = requests.post(os.getenv('CODE_EXEC_URL') + '/execute', data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                })
            r.raise_for_status()
            if r.status_code == 200:
                r = r.json()
                print('r => ', r['output'])
            print("ID => " + str(tutorial.tutorial_id))
            # tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
            # tuto['answer'] += '\n'
            # print("answer == " + tuto["answer"] + " || output == " + r["output"] + " || tutorialid == " + str(tutorial.tutorial_id))
            print("answer == '" + tuto["answer"] + "' || output == '" + r["output"] + "'")
            if tuto['answer'] == r['output']:
                check = True
            # check = False
        else:
            check = False
            tuto = TutorialService.get_tutorial(tutorial.tutorial_id)
        # print(((check == True or tuto['answer'] == tutorial.source_code)))
        if (tuto != None and (check == True or tuto['answer'] == tutorial.source_code)):
            result = TutorialService.validate_tutorial(jwt['uuid'], tutorial.tutorial_id, tutorial.language, tutorial.characters, tutorial.lines)
            print("result => ", result)
            # FETCH si None insert otherwise update
            fetch = userTutorialScoreDb.fetch(jwt['uuid'], tutorial.tutorial_id, tutorial.language)
            lang_diff = userTutorialScoreDb.fetch_all_score_of_user_by_tutorial_id(jwt['uuid'], tutorial.tutorial_id)
            langlist = []
            print(lang_diff)
            for i in range(len(lang_diff)):
                langlist.append(lang_diff[i]['language'])
                print(lang_diff[i]['language'])
            print(langlist)
            if (fetch == None): # ou tuto pas validé dans le language ?
                print("check")
                newScore = userTutorialScoreDb.insert(jwt['uuid'], tutorial.tutorial_id, tutorial.language, tutorial.characters, tutorial.lines)
                print(newScore)
            else:
                if (tutorial.characters < fetch['characters'] and tutorial.lines < fetch['lines']):
                    print("both")
                    print("lang : " + tutorial.language)
                    print("Complete ")
                    print("Characters" + str(tutorial.characters) + " || " + str(fetch['characters']))
                    print("Lines" + str(tutorial.lines) + " || " + str(fetch['lines']))
                    updateScore = userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, tutorial.characters, tutorial.lines)
                elif (tutorial.characters < fetch['characters'] and tutorial.lines >= fetch['lines']):
                    print("characters") 
                    updateScore = userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, tutorial.characters, -1)
                elif (tutorial.characters >= fetch['characters'] and tutorial.lines < fetch['lines']):
                    print("lines")
                    updateScore = userTutorialScoreDb.update(jwt['uuid'], tutorial.tutorial_id, 100, tutorial.language, -1, tutorial.lines)
            userTutorialScoreDb.close()
            return JSONResponse({'is_correct': True, 'total_completions': result, 'error': None})
        else:
            return JSONResponse({'is_correct': False, 'total_completions': 0, 'error': r['error'], "received": r['output']})
    else:
        return JSONResponse({'error': 'Missing source code or language'}, status_code=400)
