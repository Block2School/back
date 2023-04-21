from pydantic import BaseModel

class SubmitTutorialModel(BaseModel):
    source_code: str = None
    tutorial_id: int
    total_completions:int
    language: str = None
    characters :int
    lines:int
    exec:bool