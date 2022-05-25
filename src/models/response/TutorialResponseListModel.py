from pydantic import BaseModel
from models.response.TutorialResponseModel import TutorialResponseModel

class TutorialResponseListModel(BaseModel):
    data: list[TutorialResponseModel]