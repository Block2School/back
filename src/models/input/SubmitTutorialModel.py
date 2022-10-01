from pydantic import BaseModel

class SubmitTutorialModel(BaseModel):
    source_code: str = None
    tutorial_id: int
    is_already_checked: bool
    language: str = None
    characters :int
    lines:int