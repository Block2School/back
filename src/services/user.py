from urllib import response
from datetime import datetime
from database.Database import Database
from database.AccountDetails import AccountDetails
from database.Account import AccountDatabase
from services.utils.GenerateAuthenticator import GenerateAuthenticator
from database.Friends import Friends
import pyotp

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        accountDetailDb: AccountDetails = Database.get_table("account_details")
        accountDb: AccountDatabase = Database.get_table("account")
        response = accountDetailDb.fetch(uuid)
        accountDetailDb.close()
        user = accountDb.fetch(uuid)
        accountDb.close()
        return {
            "wallet": response['wallet_address'],
            "username": response['username'],
            "email": response['email'],
            "description": response['description'],
            "twitter": response['twitter'],
            "youtube": response['youtube'],
            "birthdate": datetime.timestamp(response['birthdate']) if response['birthdate'] != None else None,
            "privacy": response['private'],
            "points": user['points'],
            "uuid": uuid
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: int, private: str) -> bool:
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
            print(birthdate)
        if private != None:
            if private == "public" or private == "private" or private == "friends":
                profile['private'] = private
        response = accountDetailDb.update(uuid, profile.get('username'), profile.get('email'), profile.get('description'), profile.get('twitter'), profile.get('youtube'), profile.get('birthdate'), profile.get('private'))
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
    def get_user_privacy(uuid: str, name: str) -> str:
        accountDb: AccountDetails = Database.get_table("account_details")
        privacy = accountDb.fetch_privacy(name)
        if privacy != None:
            if privacy['private'] == "private":
                accountDb.close()
                return None
            elif privacy['private'] == "friends":
                friendsDb: Friends = Database.get_table("friends")
                is_friends = friendsDb.fetch(uuid, privacy['uuid'])
                if is_friends != None:
                    if is_friends['status'] != 'pending':
                        result = accountDb.fetch(privacy['uuid'])
                        friendsDb.close()
                        accountDb.close()
                        return result
                    accountDb.close()
                friendsDb.close()
                return None
            else:
                result = accountDb.fetch(privacy['uuid'])
                accountDb.close()
                return result
        return None

    @staticmethod
    def add_totp(uuid: str, wordlist: str) -> str:
        accountDb: AccountDatabase = Database.get_table("account")
        accountDetailsDb: AccountDetails = Database.get_table("account_details")
        account = accountDb.fetch(uuid)
        if account['discord_tag'] != None or account['qr_secret'] != None:
            accountDb.close()
            accountDetailsDb.close()
            return None
        if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
            accountDetails = accountDetailsDb.fetch(uuid)
            secret_key = pyotp.random_base32()
            qr_code = pyotp.totp.TOTP(secret_key).provisioning_uri(name=accountDetails['username'], issuer_name="Block2School")
            accountDb.update(uuid, account['is_banned'], None, None, secret_key)
            accountDb.close()
            accountDetailsDb.close()
            return qr_code
        else:
            accountDb.close()
            accountDetailsDb.close()
            return None

    @staticmethod
    def remove_totp(uuid: str, wordlist: str) -> bool:
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
        if account['qr_secret'] == None:
            accountDb.close()
            return False
        if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
            accountDb.update(uuid, account['is_banned'], None, None, None)
            accountDb.close()
            return True

    @staticmethod
    def add_discord_tag(uuid: str, discord_tag: str, wordlist: str = None) -> bool:
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
        print(account['authenticator_revoke_list'])
        print(wordlist)
        if account['discord_tag'] == None and account['qr_secret'] == None:
            if account['authenticator_revoke_list'] != None: # Need to have the wordlist to create the authenticator
                if wordlist != None:
                    if GenerateAuthenticator.signAuthenticator(wordlist) == account['authenticator_revoke_list']:
                        accountDb.update(uuid, account['is_banned'], discord_tag, None, None)
                        accountDb.close()
                        return True
                    else:
                        accountDb.close()
                        return False # Bad wordlist
                else:
                    accountDb.close()
                    return False # Need a wordlist to create the authenticator
            else:
                accountDb.update(uuid, account['is_banned'], discord_tag, None, None)
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
                accountDb.update(uuid, account['is_banned'], None, None, None)
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
        detailsDb: AccountDetails = Database.get_table("account_details")
        friends = friendsDb.fetchall(uuid)
        for i in range(0, len(friends)):
            details = detailsDb.fetch(friends[i]['friend_uuid'])
            friends[i]['username'] = details['username'] if details != None else friends[i]['friend_uuid']
            del friends[i]['uuid']
        friendsDb.close()
        return friends

    @staticmethod
    def search_user(user: str, page: int, offset: int) -> dict:
        accountDb: AccountDetails = Database.get_table("account_details")
        if page < 1 or offset < 1:
            return None
        start = offset * (page - 1)
        result = accountDb.search_user(user, start, offset)
        if not result:
            accountDb.close()
            return None
        datas = {
            "total": result[1]["total"],
            "datas": result[0]
        }
        accountDb.close()
        return datas