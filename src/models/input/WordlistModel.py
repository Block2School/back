from pydantic import BaseModel

class WordlistModel(BaseModel):
    wordlist: str = None