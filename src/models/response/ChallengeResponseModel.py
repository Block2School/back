from pydantic import BaseModel

class ChallengeResponseModel(BaseModel):
    id: int
    title: str = None
    markdown_url: str
    start_code: str
    points: int
    language: str = "python"
    inputs: list[str]
    answers: list[str]

class ChallengeResponseModelV2(BaseModel):
    id: int
    title: str = None
    markdown_url: str
    start_code: str
    points: int
    language: str = "python"
    inputs: list[str]
    answers: list[str]
    already_completed: bool = False
    completed_at: str = None

class ChallengeCompletionStatusReponseModel(BaseModel):
    already_completed: bool = False
    completed_at: str = None