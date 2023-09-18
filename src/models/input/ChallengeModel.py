from pydantic import BaseModel

class ChallengeModel(BaseModel):
    title: str = ""
    inputs: list[str]
    answers: list[str]
    markdown_url: str
    start_code: str = ""
    points: int
    language: str = "python"