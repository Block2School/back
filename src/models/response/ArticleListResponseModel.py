from pydantic import BaseModel
from models.response.ArticleResponseModel import ArticleResponseModel

class ArticleListResponseModel(BaseModel):
    data: list[ArticleResponseModel]