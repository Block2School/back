from urllib import response
from datetime import datetime
from database.AccountDetails import accountDetailDb

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        response = accountDetailDb.fetch(uuid)
        return {
            "wallet": response['wallet_address'],
            "username": response['username'],
            "email": response['email'],
            "description": response['description'],
            "twitter": response['twitter'],
            "youtube": response['youtube'],
            # "birthdate": datetime.date(response['birthdate'])
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: str) -> bool:
        profile = accountDetailDb.fetch(uuid)
        if username != None:
            profile['username'] = username
        if email != None:
            profile['email'] = email
        if description != None:
            profile['description'] = description
        if twitter != None:
            profile['twitter'] = twitter
        if youtube != None:
            profile['youtube'] = youtube
        # if birthdate != None:
        #     profile['birthdate'] = birthdate
        print(profile)
        response = accountDetailDb.update(uuid, profile.get('username'), profile.get('email'), profile.get('description'), profile.get('twitter'), profile.get('youtube'))
        return len(response) > 0