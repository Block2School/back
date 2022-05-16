from pydantic import BaseModel

class BannedResponseModel(BaseModel):
    reason: str = None
    expires: int = -1