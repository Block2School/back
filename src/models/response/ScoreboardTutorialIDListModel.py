from pydantic import BaseModel
from models.response.ScoreboardTutorialIDModel import ScoreboardTutorialIDModel

class ScoreboardTutorialIDListModel(BaseModel):
    data: list[ScoreboardTutorialIDModel]