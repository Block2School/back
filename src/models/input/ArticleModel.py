from pydantic import BaseModel

class ArticleModel(BaseModel):
    id: int = -1
    title: str
    markdownUrl: str
    author: str
    shortDescription: str