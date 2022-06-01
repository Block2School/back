from pydantic import BaseModel
from models.response.CategoryResponseModel import CategoryResponseModel

class CategoryResponseListModel(BaseModel):
    data: list[CategoryResponseModel]