from pydantic import BaseModel

class AccountTutorialCompletionModel(BaseModel):
    uuid: str
    tutorial_id: int
    total_completions: int
    last_completion: float