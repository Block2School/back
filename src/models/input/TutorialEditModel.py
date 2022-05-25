from pydantic import BaseModel

class TutorialEditModel(BaseModel):
    id: int = None
    title: str = None
    markdownUrl: str = None
    category: str = None
    answer: str = None
    startCode: str = None
    shouldBeCheck: bool = None