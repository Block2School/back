from pydantic import BaseModel
from models.response.ScoreboardTutorialIDModel import ScoreboardTutorialIDModel

class ScoreboardTutorialMeListModel(BaseModel):
    data: list[ScoreboardTutorialIDModel]