from urllib import response
from database.AccountDetails import accountDetailDb

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        response = accountDetailDb.fetch(uuid)
        return {
            "wallet": response['wallet_address'],
            "username": response['username'],
            "email": response['email']
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str) -> bool:
        response = accountDetailDb.update(uuid, username, email)
        return len(response) > 0