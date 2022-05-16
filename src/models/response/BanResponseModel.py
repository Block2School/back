from pydantic import BaseModel

class BanResponseModel(BaseModel):
    uuid: str
    banned_by: str
    reason: str
    expires: int