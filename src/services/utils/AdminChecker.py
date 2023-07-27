from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.utils.JWT import JWT
from database.Database import Database
from database.AccountModeration import AccountModeration
from services.utils.Log import Log

class AdminChecker(HTTPBearer):
    def __init__(self, needed_permission: int, auto_error: bool = True):
        self.needed_permission = needed_permission
        super(AdminChecker, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AdminChecker, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=401, detail="Invalid token scheme")
            if not self.jwt_is_correct(request, credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token")
            if not self.user_has_permission(request, credentials.credentials):
                raise HTTPException(status_code=401, detail="Permission denied")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code")

    def user_has_permission(self, request: Request, token: str) -> bool:
        accountModerationDb: AccountModeration = Database.get_table("account_moderation")
        payload = JWT.decodeJWT(token)
        user_uuid = payload.get('uuid')
        permission = accountModerationDb.fetch(user_uuid)

        accountModerationDb.close()
        if permission == None:
            Log.jwt_log(request, user_uuid, True)
            return False
        if permission['role'] >= self.needed_permission:
            return True
        Log.jwt_log(request, user_uuid, True)
        return False

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