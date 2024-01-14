from pydantic import BaseModel
from models.response.ForumCommentResponseModel import ForumCommentResponseModel

class ForumCommentResponseListModel(BaseModel):
    data: list[ForumCommentResponseModel]