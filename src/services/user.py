from datetime import datetime
from database.CompletedTutorials import CompletedTutorials
from database.Database import Database
from database.AccountDetails import AccountDetails
from database.Account import AccountDatabase
from database.Tutorials import Tutorials
from services.utils.GenerateAuthenticator import GenerateAuthenticator
from database.Friends import Friends
import pyotp

class UserService():
    @staticmethod
    def get_profile(uuid: str) -> dict:
        """
        Récupérer le profil d'un utilisateur
        """
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
    def get_profileV2(uuid: str, n: int) -> dict:
        accountDetailDb: AccountDetails = Database.get_table("account_details")
        tutorialDB: Tutorials = Database.get_table("tutorials")
        accountDb: AccountDatabase = Database.get_table("account")
        completed_tutorialsDb: CompletedTutorials = Database.get_table("completed_tutorials")
        response = accountDetailDb.fetch(uuid)
        completed = completed_tutorialsDb.get_user_n_completed_tutorials(uuid, n)
        nb_completed_tutorials = completed_tutorialsDb.get_number_completed_tutorials(uuid)
        total_nb_tutorials = tutorialDB.get_total_nb_of_tutorials()
        accountDetailDb.close()
        completed_tutorialsDb.close()
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
            "last_completed_tutorials": completed,
            "uuid": uuid,
            "nb_completed_tutorials": nb_completed_tutorials,
            "total_nb_tutorials": total_nb_tutorials,
        }

    @staticmethod
    def update_profile(uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: int, private: str) -> bool:
        """
        Modifier le profil d'un utilisateur
        """
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
        if private != None:
            if private == "public" or private == "private" or private == "friends":
                profile['private'] = private
        response = accountDetailDb.update(uuid, profile.get('username'), profile.get('email'), profile.get('description'), profile.get('twitter'), profile.get('youtube'), profile.get('birthdate'), profile.get('private'))
        accountDetailDb.close()
        return len(response) > 0

    @staticmethod
    def activate_authenticator(uuid: str) -> str:
        """
        Activer la double authentification
        """
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
        """
        Récupérer le profil d'un utilisateur (en vérifiant si l'utilisateur est autorisé)
        """
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
        """
        Ajouter la double authentification TOTP
        """
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
        """
        Supprimer la double authentification TOTP
        """
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
        """
        @deprecated

        Ajouter un tag discord pour l'utilisateur pour la double authentification discord
        """
        accountDb: AccountDatabase = Database.get_table("account")
        account = accountDb.fetch(uuid)
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
        """
        @deprecated

        Supprimer le tag discord d'un utilisateur utilisé pour la double authentification
        """
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
        """
        Ajouter un ami
        """
        friendsDb: Friends = Database.get_table("friends")
        if uuid == uuid_friend:
            friendsDb.close()
            return None
        friend = friendsDb.fetch(uuid, uuid_friend)
        if friend != None and (friend["status"] == "pending" or friend["status"] == "friend"):
            friendsDb.close()
            return None
        already_pending_other = friendsDb.fetch(uuid_friend, uuid)
        if already_pending_other != None:
            if friendsDb.update(uuid_friend, uuid, "friend") == None:
                friendsDb.close()
                return None
            if friendsDb.update(uuid, uuid_friend, "friend") == False:
                friendsDb.close()
                return None
            friendsDb.close()
            return "friend"
        else:
            if friendsDb.insert(uuid, uuid_friend, "pending") != False:
                friendsDb.insert(uuid_friend, uuid, "asking")
                friendsDb.close()
                return "pending"
            friendsDb.close()
            return None

    @staticmethod
    def remove_friend(uuid: str, uuid_friend: str) -> bool:
        """
        Supprimer un ami
        """
        friendsDb: Friends = Database.get_table("friends")
        if uuid == uuid_friend:
            friendsDb.close()
            return False
        friend = friendsDb.fetch(uuid, uuid_friend)
        if friend != None and friend["status"] == "pending":
            friendsDb.remove(uuid, uuid_friend)
            friendsDb.remove(uuid_friend, uuid)
            friendsDb.close()
            return True
        elif friend != None and friend["status"] == "friend":
            friendsDb.update(uuid, uuid_friend, "asking")
            friendsDb.update(uuid_friend, uuid, "pending")
            friendsDb.close()
            return True
        else:
            friendsDb.close()
            return False

    @staticmethod
    def get_friend_list(uuid: str) -> list:
        """
        Récupérer la liste d'amis de l'utilisateur
        """
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
        """
        Rechercher un utilisateur par son nom.
        """
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

    @staticmethod
    def get_username(uuid: str) -> str:
        """
        Récupérer le nom d'un utilisateur
        """
        accountDb: AccountDetails = Database.get_table("account_details")
        result = accountDb.get_username(uuid)
        accountDb.close()
        return result
    
    @staticmethod
    def has_authenticator(uuid: str) -> bool:
        """
        Vérifier si l'utilisateur a un authenticator
        """
        accountDb: AccountDatabase = Database.get_table("account")
        result = accountDb.fetch(uuid)
        accountDb.close()
        if result.get("qr_secret"):
            return True
        return False