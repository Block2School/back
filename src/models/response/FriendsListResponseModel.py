from pydantic import BaseModel
from models.response.FriendResponseModel import FriendResponseModel

class FriendsListResponseModel(BaseModel):
    data: list[FriendResponseModel]