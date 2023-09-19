from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse

import requests, os, json
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

router = APIRouter(prefix="/challenges")


@router.get("/leaderboard", tags=["challenges"], responses=get_leaderboard_response)
async def get_leaderboard(r: Request):
    Log.route_log(r, "challenges routes", "open_route")
    leaderboard = ChallengesService.get_leaderboard()
    return leaderboard


@router.get(
    "/leaderboard/me", tags=["challenges"], responses=get_leaderboard_by_id_response
)
async def get_user_leaderboard_rank(r: Request, jwt: JWT = Depends(JWTChecker())):
    Log.route_log(r, "challenges routes", "auth_route")
    _jwt: dict = JWT.decodeJWT(jwt)

    leaderboard = ChallengesService.get_user_leaderboard_rank(_jwt["uuid"])
    return leaderboard


@router.post("/add", tags=["challenges"], responses=create_challenge_response)
async def create_challenge(
    r: Request, challenge: ChallengeModel, jwt: JWT = Depends(JWTChecker())
):
    Log.route_log(r, "challenges routes", "auth_route")
    print(challenge)

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
    return success


@router.get(
    "/start_challenge", tags=["challenges"], responses=get_random_challenge_response
)
async def get_random_challenge(r: Request):
    Log.route_log(r, "challenges routes", "open_route")
    challenge = ChallengesService.get_random_challenge()
    challenge["inputs"] = json.loads(challenge["inputs"])
    challenge["answers"] = json.loads(challenge["answers"])
    return challenge


@router.get(
    "/start_challenge/v2", tags=["challenges"], responses=get_random_challenge_response_v2
)
async def get_random_challenge_v2(r: Request, jwt: JWT = Depends(JWTChecker())):
    Log.route_log(r, "challenges routes", "auth_route")

    _jwt: dict = JWT.decodeJWT(jwt)

    challenge = ChallengesService.get_random_challenge()
    challenge["inputs"] = json.loads(challenge["inputs"])
    challenge["answers"] = json.loads(challenge["answers"])
    completed = ChallengesService.get_completed_challenge(
        _jwt["uuid"], challenge["id"]
    )
    if completed != None:
        challenge["already_completed"] = True
        print(completed)
        challenge["completed_at"] = completed["completed_at"]
    else:
        challenge["already_completed"] = False
        challenge["completed_at"] = None
    return challenge

@router.get(
    "/is_already_completed/{id}", tags=["challenges"], responses=get_completion_status_response
)
async def check_completion_status(r: Request, challenge_id: int, jwt: JWT = Depends(JWTChecker())):
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
                }
            )
        else:
            return JSONResponse({"already_completed": False, "completed_at": None})

@router.get(
    "/challenges_input/{id}",
    tags=["challenges"],
    responses=get_random_challenge_response,
)
async def get_challenge_inputs(r: Request, id: int):
    Log.route_log(r, "challenges routes", "open_route")
    challenge = ChallengesService.get_challenge_inputs(id)
    return challenge


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
):
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
            "language": challenge["language"],
            "input": input_to_test,
        }
        print(data)
        data = json.dumps(data)
        res = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )
        print(res)
        print(res.text)
        print(res.content)
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
                    }
                )
            else:
                return JSONResponse(
                    {
                        "success": False,
                        "output": res["output"],
                        "expected_output": expected_output,
                        "error_description": res["error"],
                    }
                )
        else:
            return JSONResponse(
                {"error": "An error occured while testing the challenge"},
                status_code=400,
            )


@router.post(
    "/submit_challenge/{id}", tags=["challenges"], responses=submit_challenge_response
)
async def submit_challenge(
    r: Request,
    challenge_id: int,
    user_submit: ChallengeTestModel,
    jwt: str = Depends(JWTChecker()),
):
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
                "language": challenge["language"],
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
                if res["output"] != challenge["answers"][i]:
                    return JSONResponse(
                        {
                            "success": False,
                            "output": res["output"],
                            "expected_output": challenge["answers"][i],
                            "error_description": res["error"],
                            "test_number": i + 1,
                        }
                    )
            else:
                return JSONResponse(
                    {"error": "An error occured while testing the challenge"},
                    status_code=400,
                )
        print(_jwt["uuid"])
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
            }
        )