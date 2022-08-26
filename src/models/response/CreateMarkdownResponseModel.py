from pydantic import BaseModel

class CreateMarkdownResponseModel(BaseModel):
    success: str
    markdown_url: str