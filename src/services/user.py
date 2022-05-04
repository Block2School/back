from urllib import response
from database.AccountDetails import accountDetailDb

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        response = accountDetailDb.fetch(uuid)[0]
        return {
            "wallet": response[0],
            "username": response[1],
            "email": response[2]
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str) -> bool:
        response = accountDetailDb.update(uuid, username, email)
        return len(response) > 0