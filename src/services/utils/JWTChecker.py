from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.utils.JWT import JWT

class JWTChecker(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTChecker, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTChecker, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token scheme")
            if not self.jwt_is_correct(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

    def jwt_is_correct(self, token: str) -> bool:
        payload = JWT.decodeJWT(token)

        try:
            if payload != None:
                return True
            else:
                return False
        except:
            return False