from pydantic import BaseModel
from models.response.FaqResponseModel import FaqResponseModel

class FaqListResponseModel(BaseModel):
    data: list[FaqResponseModel]