from pydantic import BaseModel

class FriendResponseModel(BaseModel):
    friend_uuid: str
    status: str