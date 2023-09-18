from pydantic import BaseModel

class LeaderboardUserModel(BaseModel):
    user_uuid: str
    username: str
    points: int
    rank: int = None