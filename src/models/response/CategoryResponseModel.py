from pydantic import BaseModel

class CategoryResponseModel(BaseModel):
    name: str
    description: str
    image: str