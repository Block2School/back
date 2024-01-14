from pydantic import BaseModel

class ForumPostResponseModel(BaseModel):
    id: int
    title: str = None
    author_uuid: int
    description: str = None
    points: int = None
    image: str = None
    category: str
    created_at: float