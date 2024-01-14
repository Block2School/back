from pydantic import BaseModel

class ForumCommentResponseModel(BaseModel):
    post_id: int
    author_id: int
    text: str = None
