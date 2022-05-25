from pydantic import BaseModel

class ToggleTutorialResponseModel(BaseModel):
    id: int
    enabled: bool