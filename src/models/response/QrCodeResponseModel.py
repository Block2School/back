from pydantic import BaseModel

class QrCodeResponseModel(BaseModel):
    qr: str
    wordlist: str