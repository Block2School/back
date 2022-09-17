from pydantic import BaseModel

class markdownObj(BaseModel):
    title: str
    markdown_url: str

class AvailableMarkdownResponseModel(BaseModel):
    success: str
    markdowns: list[markdownObj]

