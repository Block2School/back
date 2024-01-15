from pydantic import BaseModel

class LeaderboardUserModel(BaseModel):
    user_uuid: str
    username: str
    points: int
    rank: int = None

class LeaderboardUserModel2(BaseModel):
    user_uuid: str
    username: str
    wallet_address: str
    points: int
    rank: int = None