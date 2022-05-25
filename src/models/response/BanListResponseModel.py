from pydantic import BaseModel

class BannedUser(BaseModel):
    reason: str
    banned_by: str
    expires: int
    is_revoked: bool
    revoked_by: str
    revoke_reason: str

class BanListResponseModel(BaseModel):
    data: list[BannedUser]