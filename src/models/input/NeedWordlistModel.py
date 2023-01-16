from pydantic import BaseModel

class NeedWordListModel(BaseModel):
    wordlist: str