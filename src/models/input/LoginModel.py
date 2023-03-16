from pydantic import BaseModel

class LoginModel(BaseModel):
  wallet_address: str = None
  encrypted_wallet: str = None
  token: str = None