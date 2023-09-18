from pydantic import BaseModel

from models.response.LeaderboardUserModel import LeaderboardUserModel

class LeaderboardByIDResponseModel(BaseModel):
    LeaderboardUserModel