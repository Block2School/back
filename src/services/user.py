from urllib import response
from datetime import datetime
from database.AccountDetails import accountDetailDb
from database.Account import accountDb
from services.utils.GenerateAuthenticator import GenerateAuthenticator

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
            "birthdate": datetime.timestamp(response['birthdate'])
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: int) -> bool:
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
        if birthdate != None:
            profile['birthdate'] = datetime.fromtimestamp(birthdate)
        response = accountDetailDb.update(uuid, profile.get('username'), profile.get('email'), profile.get('description'), profile.get('twitter'), profile.get('youtube'), profile.get('birthdate'))
        return len(response) > 0

    @staticmethod
    def activate_authenticator(uuid: str) -> str:
        account = accountDb.fetch(uuid)
        if account['authenticator_revoke_list'] == None:
            wordlist = GenerateAuthenticator.generate_authenticator()
            accountDb.add_revoke_word_list(uuid, GenerateAuthenticator.signAuthenticator(wordlist))
            return wordlist
        else:
            return None

    @staticmethod
    def add_discord_tag(uuid: str, discord_tag: str, wordlist: str = None) -> bool:
        account = accountDb.fetch(uuid)
        print(account['authenticator_revoke_list'])
        print(wordlist)
        if account['discord_tag'] == None:
            if account['authenticator_revoke_list'] != None: # Need to have the wordlist to create the authenticator
                if wordlist != None:
                    if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
                        accountDb.update(uuid, account['is_banned'], discord_tag, None)
                        return True
                    else:
                        return False # Bad wordlist
                else:
                    return False # Need a wordlist to create the authenticator
            else:
                accountDb.update(uuid, account['is_banned'], discord_tag, None)
                return True
        else:
            return False # Already linked

    @staticmethod
    def remove_discord_tag(uuid: str, wordlist: str) -> bool:
        account = accountDb.fetch(uuid)
        if account['discord_tag'] != None:
            if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
                accountDb.update(uuid, account['is_banned'], None, None)
                return True
            else:
                return False # Bad wordlist
        else:
            return False # No discord tag