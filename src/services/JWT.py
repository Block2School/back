from time import time
from typing import Dict
import jwt
import os

class JWT():
  @staticmethod
  def signJWT(uuid: str) -> Dict[str, str]:
    payload = {
      "uuid": uuid,
      "expires": time() + 7200
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
    return token

  @staticmethod
  def decodeJWT(token: str) -> dict:
    try:
      decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=os.getenv('JWT_ALGORITHM'))
      if decoded_token.get('expires') >= time.time():
        return decoded_token
      else:
        return None
    except:
      return None