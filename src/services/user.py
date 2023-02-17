from urllib import response
from datetime import datetime
from database.Account import AccountDatabase
from database.Database import Database
from database.AccountDetails import AccountDetails
from services.utils.GenerateAuthenticator import GenerateAuthenticator
from database.Friends import Friends

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        accountDetailDb: AccountDetails = Database.get_table("account_details")
        response = accountDetailDb.fetch(uuid)
        accountDetailDb.close()
        return {
            "wallet": response['wallet_address'],
            "username": response['username'],
            "email": response['email'],
            "description": response['description'],
            "twitter": response['twitter'],
            "youtube": response['youtube'],
            "birthdate": datetime.timestamp(response['birthdate']) if response['birthdate'] != None else None
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: int) -> bool:
        accountDetailDb: AccountDetails = Database.get_table("account_details")
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
        accountDetailDb.close()
        return len(response) > 0

    @staticmethod
    def activate_authenticator(uuid: str) -> str:
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
        if account['authenticator_revoke_list'] == None:
            wordlist = GenerateAuthenticator.generate_authenticator()
            accountDb.add_revoke_word_list(uuid, GenerateAuthenticator.signAuthenticator(wordlist))
            accountDb.close()
            return wordlist
        else:
            accountDb.close()
            return None

    @staticmethod
    def add_discord_tag(uuid: str, discord_tag: str, wordlist: str = None) -> bool:
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
        if account['discord_tag'] == None:
            if account['authenticator_revoke_list'] != None: # Need to have the wordlist to create the authenticator
                if wordlist != None:
                    if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
                        accountDb.update(uuid, account['is_banned'], discord_tag, None)
                        accountDb.close()
                        return True
                    else:
                        accountDb.close()
                        return False # Bad wordlist
                else:
                    accountDb.close()
                    return False # Need a wordlist to create the authenticator
            else:
                accountDb.update(uuid, account['is_banned'], discord_tag, None)
                accountDb.close()
                return True
        else:
            accountDb.close()
            return False # Already linked

    @staticmethod
    def remove_discord_tag(uuid: str, wordlist: str) -> bool:
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
        if account['discord_tag'] != None:
            if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
                accountDb.update(uuid, account['is_banned'], None, None)
                accountDb.close()
                return True
            else:
                accountDb.close()
                return False # Bad wordlist
        else:
            accountDb.close()
            return False # No discord tag

    @staticmethod
    def add_friend(uuid: str, uuid_friend: str) -> str:
        friendsDb: Friends = Database.get_table("friends")
        if uuid == uuid_friend:
            friendsDb.close()
            return None
        friend = friendsDb.fetch(uuid, uuid_friend)
        if friend != None:
            friendsDb.close()
            return None
        already_pending_other = friendsDb.fetch(uuid_friend, uuid)
        if already_pending_other != None:
            if friendsDb.update(uuid_friend, uuid, "friend") == None:
                friendsDb.close()
                return None
            if friendsDb.insert(uuid, uuid_friend, "friend") == False:
                friendsDb.close()
                return None
            friendsDb.close()
            return "friend"
        else:
            if friendsDb.insert(uuid, uuid_friend, "pending") != False:
                friendsDb.close()
                return "pending"
            friendsDb.close()
            return None

    @staticmethod
    def remove_friend(uuid: str, uuid_friend: str) -> bool:
        friendsDb: Friends = Database.get_table("friends")
        if uuid == uuid_friend:
            friendsDb.close()
            return False
        friend = friendsDb.fetch(uuid, uuid_friend)
        if friend != None:
            friendsDb.remove(uuid, uuid_friend)
            if friendsDb.fetch(uuid_friend, uuid) != None:
                friendsDb.update(uuid_friend, uuid, "pending")
            friendsDb.close()
            return True
        else:
            friendsDb.close()
            return False

    @staticmethod
    def get_friend_list(uuid: str) -> list:
        friendsDb: Friends = Database.get_table("friends")
        friends = friendsDb.fetchall(uuid)
        for i in range(0, len(friends)):
            del friends[i]['uuid']
        friendsDb.close()
        return friends