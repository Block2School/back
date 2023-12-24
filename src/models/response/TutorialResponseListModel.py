from pydantic import BaseModel
from models.response.TutorialResponseModel import TutorialResponseModel, TutorialResponseModelV2

class TutorialResponseListModel(BaseModel):
    data: list[TutorialResponseModel]

class TutorialResponseListModelV2(BaseModel):
    data: list[TutorialResponseModelV2]