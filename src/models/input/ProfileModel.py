from pydantic import BaseModel

class ProfileModel(BaseModel):
    username: str
    email: str