from pydantic import BaseModel

from models.response.LeaderboardUserModel import LeaderboardUserModel, LeaderboardUserModel2

class LeaderboardResponseModel(BaseModel):
    data: list[LeaderboardUserModel]

class LeaderboardResponseModel2(BaseModel):
    data: list[LeaderboardUserModel2]