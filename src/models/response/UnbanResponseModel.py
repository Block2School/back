from pydantic import BaseModel

class UnbanResponseModel(BaseModel):
    uuid: str
    revoked_by: str
    reason: str