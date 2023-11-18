from pydantic import BaseModel

class LastCompletedTutorialModel(BaseModel):
    title: str
    tutorial_id: str