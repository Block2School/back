from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.login import LoginService
from services.utils.JWT import JWT
from services.utils.Log import Log

class JWTChecker(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTChecker, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTChecker, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=401, detail="Invalid token scheme")
            if not self.jwt_is_correct(request, credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token")
            if self.check_banned(request, credentials.credentials) == True:
                raise HTTPException(status_code=403, detail="User is banned")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code")

    def jwt_is_correct(self, request: Request, token: str) -> bool:
        payload = JWT.decodeJWT(token)

        try:
            if payload != None:
                return True
            else:
                Log.jwt_log(request)
                return False
        except:
            Log.jwt_log(request)
            return False

    def check_banned(self, request: Request, token: str) -> bool:
        payload = JWT.decodeJWT(token)

        # check if the user is banned
        is_banned = LoginService.is_banned(payload['uuid'])
        print('is_banned', is_banned)
        if is_banned != None:
            Log.login_log(request, payload['uuid'], False, True)
            return True
        else:
            return False