from pydantic import BaseModel

class CategoryResponseModel(BaseModel):
    name: str
    tutorials_number: int