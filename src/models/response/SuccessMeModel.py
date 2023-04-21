from pydantic import BaseModel
from models.response.ScoreboardTutorialIDModel import ScoreboardTutorialIDModel

class SuccessMeModel(BaseModel):
    data: list[ScoreboardTutorialIDModel]
    total_completion: float