from pydantic import BaseModel

class CompleteTutorialResponseModel(BaseModel):
    is_correct: bool
    total_completions: int
    error_description: str