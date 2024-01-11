from pydantic import BaseModel

class LeaveChallengeRoomModel(BaseModel):
    user_uuid: str