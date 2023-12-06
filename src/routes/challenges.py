from fastapi import APIRouter, Depends, Form, Request, WebSocket

from fastapi.responses import JSONResponse

import requests, os, json, time
from models.input.ChallengeModel import ChallengeModel
from models.input.ChallengeTestModel import ChallengeTestModel
from models.response.ChallengeResponseModel import (
    ChallengeResponseModel,
    ChallengeResponseModelV2,
    ChallengeCompletionStatusReponseModel,
)
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.LeaderboardByIDResponseModel import LeaderboardByIDResponseModel
from models.response.LeaderboardResoonseModel import LeaderboardResponseModel
from models.response.SubmitChallengeResponseModel import SubmitChallengeResponseModel
from models.response.JoinChallengeResponseModel import JoinChallengeResponseModel
from models.response.LeaveChallengeRoomModel import LeaveChallengeRoomModel
from services.challenges import ChallengesService
from services.utils.JWTChecker import JWTChecker
from services.utils.Log import Log
from services.utils.JWT import JWT

# LEADERBOARD CHALLENGE -->
get_leaderboard_response = {200: {"model": LeaderboardResponseModel}}

get_leaderboard_by_id_response = {
    200: {"model": LeaderboardByIDResponseModel},
    400: {"model": ErrorResponseModel},
}

# CHALLENGE -->
get_random_challenge_response = {200: {"model": ChallengeResponseModel}}
get_random_challenge_response_v2 = {
    200: {"model": ChallengeResponseModelV2},
    400: {"model": ErrorResponseModel},
}

get_completion_status_response = {
    200: {"model": ChallengeCompletionStatusReponseModel},
    400: {"model": ErrorResponseModel},
}

submit_challenge_response = {
    200: {"model": SubmitChallengeResponseModel},
    400: {"model": ErrorResponseModel},
}

test_challenge_response = {
    200: {"model": SubmitChallengeResponseModel},
    400: {"model": ErrorResponseModel},
}

create_challenge_response = {
    200: {"model": ChallengeResponseModel},
    400: {"model": ErrorResponseModel},
}

join_challenge_response = {
    200: {"model": JoinChallengeResponseModel},
    400: {"model": ErrorResponseModel},
}

router = APIRouter(prefix="/challenges")


@router.get("/leaderboard", tags=["challenges"], responses=get_leaderboard_response)
async def get_leaderboard(r: Request) -> JSONResponse:
    """
    Récupération du leaderboard
    """
    Log.route_log(r, "challenges routes", "open_route")
    leaderboard = ChallengesService.get_leaderboard()
    return JSONResponse(leaderboard, status_code=200)


@router.get(
    "/leaderboard/me", tags=["challenges"], responses=get_leaderboard_by_id_response
)
async def get_user_leaderboard_rank(r: Request, jwt: JWT = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupération du rang de l'utilisateur dans le leaderboard des challenges
    """
    Log.route_log(r, "challenges routes", "auth_route")
    _jwt: dict = JWT.decodeJWT(jwt)

    leaderboard = ChallengesService.get_user_leaderboard_rank(_jwt["uuid"])
    return JSONResponse(leaderboard, status_code=200)

@router.get(
    "/leaderboard/top_10_monthly", tags=["challenges"], responses=get_leaderboard_response
)
async def get_top_10_monthly(r: Request) -> JSONResponse:
    """
    Récupération du top 10 des utilisateurs du mois dans les challenges
    """
    Log.route_log(r, "challenges routes", "open_route")
    leaderboard = ChallengesService.get_top_10_monthly()
    return JSONResponse(leaderboard, status_code=200)

@router.get(
    "/leaderboard/top_monthly", tags=["challenges"], responses=get_leaderboard_response
)
async def get_top_monthly(r: Request) -> JSONResponse:
    """
    Récupération du top utilisateur du mois dans les challenges
    """
    Log.route_log(r, "challenges routes", "open_route")
    leaderboard = ChallengesService.get_top_monthly()
    return JSONResponse(leaderboard, status_code=200)

@router.post("/add", tags=["challenges"], responses=create_challenge_response)
async def create_challenge(
    r: Request, challenge: ChallengeModel, jwt: JWT = Depends(JWTChecker())
) -> JSONResponse:
    """
    Création d'un challenge
    """
    Log.route_log(r, "challenges routes", "auth_route")

    if len(challenge.inputs) != len(challenge.answers):
        return JSONResponse(
            {"error": "Inputs and answers must be the same length"}, status_code=400
        )

    inputs: list = []
    answers: list = []

    for i in range(len(challenge.inputs)):
        inputs.append(challenge.inputs[i])

    for i in range(len(challenge.answers)):
        answers.append(challenge.answers[i])

    _inputs: str = json.dumps(inputs)
    _answers: str = json.dumps(answers)

    success = ChallengesService.add_challenge(
        inputs=_inputs,
        answers=_answers,
        markdown_url=challenge.markdown_url,
        start_code=challenge.start_code,
        points=challenge.points,
        title=challenge.title,
        language=challenge.language,
    )
    return JSONResponse(success, status_code=200)


@router.get(
    "/start_challenge", tags=["challenges"], responses=get_random_challenge_response
)
async def get_random_challenge(r: Request) -> JSONResponse:
    """
    Récupération d'un challenge aléatoire
    """
    Log.route_log(r, "challenges routes", "open_route")
    challenge = ChallengesService.get_random_challenge()
    challenge["inputs"] = json.loads(challenge["inputs"])
    challenge["answers"] = json.loads(challenge["answers"])
    return JSONResponse(challenge, status_code=200)


@router.get(
    "/start_challenge/v2",
    tags=["challenges"],
    responses=get_random_challenge_response_v2,
)
async def get_random_challenge_v2(r: Request, jwt: JWT = Depends(JWTChecker())) -> JSONResponse:
    """
    Récupération d'un challenge
    """
    Log.route_log(r, "challenges routes", "auth_route")

    _jwt: dict = JWT.decodeJWT(jwt)

    challenge = ChallengesService.get_random_challenge()
    challenge["inputs"] = json.loads(challenge["inputs"])
    challenge["answers"] = json.loads(challenge["answers"])
    completed = ChallengesService.get_completed_challenge(_jwt["uuid"], challenge["id"])
    if completed != None:
        challenge["already_completed"] = True
        challenge["completed_at"] = completed["completed_at"]
    else:
        challenge["already_completed"] = False
        challenge["completed_at"] = None
    return challenge


@router.get(
    "/is_already_completed/{id}",
    tags=["challenges"],
    responses=get_completion_status_response,
)
async def check_completion_status(
    r: Request, challenge_id: int, jwt: JWT = Depends(JWTChecker())
) -> JSONResponse:
    """
    Vérifier la complétion du challenge
    """
    Log.route_log(r, "challenges routes", "auth_route")

    _jwt: dict = JWT.decodeJWT(jwt)

    challenge = ChallengesService.get_challenge(challenge_id)
    if challenge == None:
        return JSONResponse({"error": "Challenge not found"}, status_code=400)
    else:
        completed = ChallengesService.get_completed_challenge(
            _jwt["uuid"], challenge["id"]
        )
        if completed != None:
            completed_at: str = str(completed["completed_at"])
            return JSONResponse(
                {
                    "already_completed": True,
                    "completed_at": completed_at,
                }, status_code=200
            )
        else:
            return JSONResponse({"already_completed": False, "completed_at": None}, status_code=200)


@router.get(
    "/challenges_input/{id}",
    tags=["challenges"],
    responses=get_random_challenge_response,
)
async def get_challenge_inputs(r: Request, id: int) -> JSONResponse:
    """
    Récupération des inputs du challenge
    """
    Log.route_log(r, "challenges routes", "open_route")
    challenge = ChallengesService.get_challenge_inputs(id)
    return JSONResponse(challenge, status_code=200)


@router.post(
    "/test_challenge/{challenge_id}/{test_number}",
    tags=["challenges"],
    responses=test_challenge_response,
)
async def test_challenge(
    r: Request,
    challenge_id: int,
    test_number: int,
    user_submit: ChallengeTestModel,
    jwt: JWT = Depends(JWTChecker()),
) -> JSONResponse:
    """
    Tester un challenge
    """
    Log.route_log(r, "challenges routes", "auth_route")
    challenge = ChallengesService.get_challenge(challenge_id)
    if challenge == None:
        return JSONResponse({"error": "Challenge not found"}, status_code=400)
    else:
        challenge["inputs"] = json.loads(challenge["inputs"])
        challenge["answers"] = json.loads(challenge["answers"])

        if test_number < 1 or test_number > len(challenge["inputs"]):
            return JSONResponse({"error": "Test number out of range"}, status_code=400)

        input_to_test: str = challenge["inputs"][test_number - 1]
        expected_output: str = challenge["answers"][test_number - 1]
        url = os.getenv("CODE_EXEC_URL") + "/execute"
        data = {
            "code": user_submit.code,
            "language": user_submit.language,
            "input": input_to_test,
        }
        data = json.dumps(data)
        res = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )
        res.raise_for_status()
        if res.status_code == 200:
            res = res.json()
            if res["output"] == expected_output:
                return JSONResponse(
                    {
                        "success": True,
                        "output": res["output"],
                        "expected_output": expected_output,
                        "error_description": res["error"],
                    }, status_code=200
                )
            else:
                return JSONResponse(
                    {
                        "success": False,
                        "output": res["output"],
                        "expected_output": expected_output,
                        "error_description": res["error"],
                    }, status_code=200
                )
        else:
            return JSONResponse(
                {"error": "An error occured while testing the challenge"},
                status_code=400,
            )


@router.post(
    "/submit_challenge/{challenge_id}",
    tags=["challenges"],
    responses=submit_challenge_response,
)
async def submit_challenge(
    r: Request,
    challenge_id: int,
    user_submit: ChallengeTestModel,
    jwt: str = Depends(JWTChecker()),
) -> JSONResponse:
    """
    Envoyer un challenge
    """
    Log.route_log(r, "challenges routes", "auth_route")
    _jwt = JWT.decodeJWT(jwt)
    challenge = ChallengesService.get_challenge(challenge_id)
    if challenge == None:
        return JSONResponse({"error": "Challenge not found"}, status_code=400)
    else:
        challenge["inputs"] = json.loads(challenge["inputs"])
        challenge["answers"] = json.loads(challenge["answers"])
        url = os.getenv("CODE_EXEC_URL") + "/execute"
        last_output = ""

        for i in range(len(challenge["inputs"])):
            data = {
                "code": user_submit.code,
                "language": user_submit.language,
                "input": challenge["inputs"][i],
            }
            data = json.dumps(data)
            res = requests.post(
                url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            )
            res.raise_for_status()
            if res.status_code == 200:
                res = res.json()
                last_output = res["output"]
                if res["output"] != challenge["answers"][i] and res["error"] != "":
                    return JSONResponse(
                        {
                            "success": False,
                            "output": res["output"],
                            "expected_output": challenge["answers"][i],
                            "error_description": res["error"],
                            "error_test_index": -1,
                            "isError": True,
                        }, status_code=200
                    )
                if res["output"] != challenge["answers"][i]:
                    return JSONResponse(
                        {
                            "success": False,
                            "output": res["output"],
                            "expected_output": challenge["answers"][i],
                            "error_description": res["error"],
                            "error_test_index": i + 1,
                            "isError": False,
                        }, status_code=200
                    )
            else:
                return JSONResponse(
                    {"error": "An error occured while testing the challenge"},
                    status_code=400,
                )
        was_completed = ChallengesService.get_completed_challenge(
            _jwt["uuid"], challenge["id"]
        )
        if was_completed != None:
            return JSONResponse(
                {
                    "success": True,
                    "output": last_output,
                    "expected_output": challenge["answers"][
                        len(challenge["answers"]) - 1
                    ],
                    "error_description": res["error"],
                    "error_test_index": -1,
                    "isError": False,
                }, status_code=200
            )
        success = ChallengesService.complete_challenge(_jwt["uuid"], challenge_id)
        if success == False:
            Log.error_log(
                "challenges routes",
                "submit_challenge",
                "complete_challenge",
                "An error occured while completing the challenge",
            )
        success = ChallengesService.add_points(_jwt["uuid"], challenge["points"])
        if success == False:
            Log.error_log(
                "challenges routes",
                "submit_challenge",
                "add_points",
                "An error occured while adding points",
            )
        return JSONResponse(
            {
                "success": True,
                "output": last_output,
                "expected_output": challenge["answers"][len(challenge["answers"]) - 1],
                "error_description": res["error"],
                "error_test_index": -1,
                "isError": False,
            }, status_code=200
        )

@router.post("/createRoom/{roomID}/{userID}")
def createRoom(roomID: int, userID: str):
    success = ChallengesService.create_room(roomID, userID)
    return success

@router.post("/deleteRoom/{roomID}")
async def delete_room(roomID: int):
    success = await ChallengesService.delete_room(roomID)
    return success

@router.websocket("/joinRoom/{roomID}/{userUUID}")
async def join_room(ws: WebSocket, roomID: int, userUUID: str):
    success = await ChallengesService.join_room(roomID, ws, userUUID)
    room = ChallengesService.get_room(roomID)
    if success:
        await room.broadcast(
            json.dumps({
                "type": "new user joined",
                "message": userUUID,
            })
        )
        await ws.accept()
        await ws.send_text(json.dumps({
            "type": "room info",
            "message": {
                "roomID": room.getRoomID(),
                "occupants": [occupant.getUserUUID() for occupant in room.getOccupants()],
                "remainingTime": room.getRemainingTime(),
                "limitUser": room.getLimitUser()
            }
        }))
        while len(room.getOccupants()) > 0:
            try:
                await ws.receive_text()
            except:
                break
    return success

@router.post("/leaveRoom/{roomID}/{user_uuid}")
async def leave_room(user_uuid: str, roomID: int):
    uuid = user_uuid
    room = ChallengesService.get_room(roomID)
    if room is None:
        return False
    users = room.getOccupants()
    if users is None:
        return False
    ws = None
    for i in range(len(users)):
        if users[i].getUserUUID() == uuid:
            ws = users[i].getWs()
    success = await ChallengesService.leave_room(roomID, uuid, ws)
    return success

@router.post("/broadcast/{roomID}")
async def broadcast(roomID: int):
    success = await ChallengesService.broadcast(roomID, json.dumps({"message": "test"}))
    return success

@router.get("/getAllRooms")
async def getAllRooms():
    rooms = ChallengesService.getAllRooms()
    json = {
        "rooms": []
    }
    for room in rooms:
        json["rooms"].append({
            "roomID": room.getRoomID(),
            "occupants": [occupant.getUserUUID() for occupant in room.getOccupants()],
            "maxTime": room.getMaxTime(),
            "limitUser": room.getLimitUser()
        })
    return json

@router.get("/getRoomById/{roomID}")
async def getRoomById(roomID: int):
    room = ChallengesService.get_room(roomID)
    if room == None:
        return {}
    json = {
        "master": room.getMaster(),
        "occupants": [occupant.getUserUUID() for occupant in room.getOccupants()],
        "maxTime": room.getMaxTime(),
        "limitUser": room.getLimitUser()
    }
    return json