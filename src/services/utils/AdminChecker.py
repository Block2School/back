from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.utils.JWT import JWT
from database.AccountModeration import accountModerationDb

class AdminChecker(HTTPBearer):
    def __init__(self, needed_permission: int, auto_error: bool = True):
        self.needed_permission = needed_permission
        super(AdminChecker, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AdminChecker, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token scheme")
            if not self.jwt_is_correct(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token")
            if not self.user_has_permission(credentials.credentials):
                raise HTTPException(status_code=401, detail="Permission denied")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

    def user_has_permission(self, token: str) -> bool:
        payload = JWT.decodeJWT(token)
        user_uuid = payload.get('uuid')
        permission = accountModerationDb.fetch(user_uuid)

        if len(permission) == 0:
            return False
        if permission[0][0] >= self.needed_permission:
            return True
        return False

    def jwt_is_correct(self, token: str) -> bool:
        payload = JWT.decodeJWT(token)

        try:
            if payload != None:
                return True
            else:
                return False
        except:
            return False