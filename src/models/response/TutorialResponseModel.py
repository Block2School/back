from pydantic import BaseModel

class TutorialResponseModel(BaseModel):
    id: int
    title: str
    markdownUrl: str
    category: str
    answer: str
    startCode: str
    shouldBeCheck: bool
    enabled: bool
    points: int