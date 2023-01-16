from pydantic import BaseModel

class ProfileResponseModel(BaseModel):
    wallet: str
    username: str
    email: str
    description: str
    twitter: str
    youtube: str
    birthdate: int