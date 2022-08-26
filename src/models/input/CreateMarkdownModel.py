from pydantic import BaseModel

class CreateMarkdownModel(BaseModel):
    name: str
    content: str