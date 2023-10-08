from pydantic import BaseModel

from models.response.LeaderboardUserModel import LeaderboardUserModel

class LeaderboardResponseModel(BaseModel):
    data: list[LeaderboardUserModel]
    