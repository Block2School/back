from database.UserAccess import userAccessDb

class UserAccess():
    @staticmethod
    def user_has_access(uuid: str, access_uuid: str, access_data: str) -> bool:
        data_protection = userAccessDb.fetch(access_uuid, access_data)
        if data_protection == 'public':
            return True
        elif data_protection == 'private':
            return False
        elif data_protection == 'friend': # WIP
            return False