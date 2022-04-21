from pydantic import BaseModel

class ProfileResponseModel(BaseModel):
    wallet: str
    username: str
    email: str