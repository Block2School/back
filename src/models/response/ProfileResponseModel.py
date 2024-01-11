from pydantic import BaseModel

from models.response.LastCompletedTutorialModel import LastCompletedTutorialModel

class ProfileResponseModel(BaseModel):
    wallet: str
    username: str
    email: str
    description: str
    twitter: str
    youtube: str
    birthdate: int

class ProfileResponseModelV2(BaseModel):
    wallet: str
    username: str
    email: str
    description: str
    twitter: str
    youtube: str
    birthdate: int
    last_completed_tutorials: list[LastCompletedTutorialModel]
    nb_completed_tutorials: int
    total_nb_tutorials: int