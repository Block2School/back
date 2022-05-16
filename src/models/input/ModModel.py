from pydantic import BaseModel

class ModModel(BaseModel):
    uuid: str = None
    role: int = -1