from pydantic import BaseModel

class FaqModel(BaseModel):
    id: int
    question: str
    answer: str