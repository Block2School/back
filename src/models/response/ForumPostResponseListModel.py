from pydantic import BaseModel
from models.response.ForumPostResponseModel import ForumPostResponseModel

class ForumPostResponseListModel(BaseModel):
    data: list[ForumPostResponseModel]

