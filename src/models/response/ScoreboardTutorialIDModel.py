from pydantic import BaseModel

class ScoreboardTutorialIDModel(BaseModel):
    uuid: str
    tutorial_id: int
    total_completions: int
    language: str
    characters: int
    lines: int