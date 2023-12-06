from time import time
from typing import Dict
import jwt
import os

class JWT():
  @staticmethod
  def signJWT(uuid: str) -> Dict[str, str]:
    """
    Créer un JWT à partir de l'UUID de l'utilisateur
    """
    payload = {
      "uuid": uuid,
      "expires": time() + 7200
    }
    token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
    if (type(token) == str) : return token
    return token.decode('utf-8')

  @staticmethod
  def decodeJWT(token: str) -> dict:
    """
    Vérifier le JWT reçu pour obtenir l'UUID de l'utilisateur et vérifier que le token n'est pas expiré.
    """
    try:
      decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=os.getenv('JWT_ALGORITHM'))
      if decoded_token.get('expires') >= time():
        return decoded_token
      else:
        return None
    except:
      return None

class RefreshToken():
    @staticmethod
    def signRefreshToken(access_token: str) -> Dict[str, str]:
        payload = {
            "token": access_token,
            "expires": time() + 2592000 # 30 days
        }
        token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm=os.getenv('JWT_ALGORITHM'))
        if (type(token) == str) : return token
        return token.decode('utf-8')

    @staticmethod
    def decodeRefreshToken(refresh_token: str) -> dict:
        try:
            decoded_token = jwt.decode(refresh_token, os.getenv('JWT_SECRET'), algorithms=os.getenv('JWT_ALGORITHM'))
            if decoded_token.get('expires') >= time():
                user_informations = JWT.decodeJWT(decoded_token['token'])
                if user_informations != None:
                    return {'uuid': user_informations['uuid']}
            else:
                return None
        except:
            return None