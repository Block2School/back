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
    image: str
    short_description: str
    default_language: str
    estimated_time: str

class TutorialResponseModelV2(BaseModel):
    id: int
    title: str
    markdownUrl: str
    category: str
    answer: str
    startCode: str
    shouldBeCheck: bool
    enabled: bool
    points: int
    image: str
    short_description: str
    default_language: str
    estimated_time: str
    is_completed: bool
