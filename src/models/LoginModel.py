from pydantic import BaseModel

class LoginModel(BaseModel):
  wallet_address: str = None