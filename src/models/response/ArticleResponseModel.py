from pydantic import BaseModel

class ArticleResponseModel(BaseModel):
    id: int
    title: str
    markdownUrl: str
    shortDescription: str
    publicationDate: float
    author: str