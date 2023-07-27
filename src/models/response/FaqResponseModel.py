from pydantic import BaseModel

class FaqResponseModel(BaseModel):
    id: int
    question: str
    answer: str