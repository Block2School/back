from pydantic import BaseModel

class BanModel(BaseModel):
    uuid: str = None
    reason: str = None
    expires: int = -1