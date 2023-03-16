from pydantic import BaseModel

class TutorialModel(BaseModel):
    title: str = None
    markdownUrl: str = None
    category: str = None
    answer: str = None
    startCode: str = None
    shouldBeCheck: bool = None
    input: str = None