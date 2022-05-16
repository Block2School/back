from pydantic import BaseModel

class UnbanModel(BaseModel):
    uuid: str = None
    reason: str = None