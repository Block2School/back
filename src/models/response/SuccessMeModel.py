from pydantic import BaseModel
from models.response.AccountTutorialCompletionModel import AccountTutorialCompletionModel

class SuccessMeModel(BaseModel):
    data: list[AccountTutorialCompletionModel]
    total_completion: float