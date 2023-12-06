from database.Database import Database
from database.UserAccess import UserAccess

class UserAccess():
    @staticmethod
    def user_has_access(uuid: str, access_uuid: str, access_data: str) -> bool:
        """
        Vérifie si l'utilisateur à bien accès à la donnée qu'il souhaite consulter.
        """
        userAccessDb: UserAccess = Database.get_table("user_access")
        data_protection = userAccessDb.fetch(access_uuid, access_data)
        if data_protection == 'public':
            return True
        elif data_protection == 'private':
            return False
        elif data_protection == 'friend': # WIP
            return False