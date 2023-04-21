from pydantic import BaseModel

class ProfileModel(BaseModel):
    username: str = None
    email: str = None
    description: str = None
    twitter: str = None
    youtube: str = None
    birthdate: int = None
    privacy: str = None