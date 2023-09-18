from pydantic import BaseModel

class ChallengeTestModel(BaseModel):
    code: str
    language: str = "python"