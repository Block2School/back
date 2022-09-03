from pydantic import BaseModel

class AccountResponseModel(BaseModel):
    uuid: str
    wallet_address: str
    is_banned: bool