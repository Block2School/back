from pydantic import BaseModel
from models.response.FaqResponseModel import FaqResponseModel

class FriendsListResponseModel(BaseModel):
    data: list[FaqResponseModel]