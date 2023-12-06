from datetime import datetime
import uuid
from database.Database import Database
from database.Account import AccountDatabase
from services.utils.JWT import JWT, RefreshToken
from services.utils.WalletHash import WalletHash
from database.AccountDetails import AccountDetails
from database.AccountPunishment import AccountPunishment
import pyotp

class LoginService():
    @staticmethod
    def check_account(encrypted_wallet: str) -> list:
        """
        Vérifier si le compte existe sur le serveur
        """
        accountDb: AccountDatabase = Database.get_table("account")
        wallet_hash = WalletHash.wallet_hash(encrypted_wallet)
        result = accountDb.login(wallet_hash)
        accountDb.close()
        if result != None:
            return [wallet_hash, result['uuid'], result['discord_tag'], result['qr_secret']]
        else:
            return [wallet_hash]

    @staticmethod
    def register(wallet_hash: str, wallet: str) -> str:
        """
        Inscription du compte sur le serveur
        """
        accountDb: AccountDatabase = Database.get_table("account")
        accountDetailDb: AccountDetails = Database.get_table("account_details")
        user_uuid = uuid.uuid4()
        if accountDb.insert(str(user_uuid), wallet_hash):
            accountDetailDb.insert(str(user_uuid), wallet)
            jwt = JWT.signJWT(str(user_uuid))
            accountDetailDb.close()
            accountDb.close()
            return jwt
        accountDetailDb.close()
        accountDb.close()
        return None

    @staticmethod
    def login(user_uuid: str, token: str = None) -> str:
        """
        Connexion de l'utilisateur sur le serveur
        """
        accountDb: AccountDatabase = Database.get_table("account")
        if token == None:
            jwt = JWT.signJWT(user_uuid)
        else:
            account = accountDb.fetch(user_uuid)
            if account['discord_token'] != None:
                try:
                    if account['discord_token'] == int(token):
                        accountDb.update(user_uuid, account['is_banned'], account['discord_tag'], None, None)
                        jwt = JWT.signJWT(user_uuid)
                    else:
                        accountDb.close()
                        return None
                except:
                    accountDb.close()
                    return None
            else:
                try:
                    totp = pyotp.TOTP(account['qr_secret'])
                    if totp.verify(token):
                        jwt = JWT.signJWT(user_uuid)
                    else:
                        accountDb.close()
                        return None
                except:
                    accountDb.close()
                    return None
        accountDb.close()
        return jwt

    @staticmethod
    def create_refresh_token(access_token: str) -> str:
        """
        Créer un refresh token pour le token JWT
        """
        refresh_token = RefreshToken.signRefreshToken(access_token)
        return refresh_token

    @staticmethod
    def is_banned(user_uuid: str) -> dict:
        """
        Vérifie si l'utilisateur est banni ou non de la plateforme
        """
        accountDb: AccountDatabase = Database.get_table("account")
        accountPunishmentDb: AccountPunishment = Database.get_table("account_punishment")
        account = accountDb.fetch(user_uuid)
        if account == None:
            accountPunishmentDb.close()
            accountDb.close()
            return None
        if account['is_banned']:
            bans = accountPunishmentDb.fetch(user_uuid)
            if len(bans) > 0:
                ban = bans[-1]
                if ban['expires'] != None:
                    if datetime.now() > ban['expires']:
                        accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'], account['qr_secret'])
                        accountDb.close()
                        accountPunishmentDb.close()
                        return None
                if not ban['is_revoked']:
                    accountDb.close()
                    accountPunishmentDb.close()
                    return {"reason": ban['reason'], "expires": datetime.timestamp(ban['expires']) if ban['expires'] else -1}
                else:
                    accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'], account['qr_secret'])
                    accountDb.close()
                    accountPunishmentDb.close()
                    return None
            else:
                accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'], account['qr_secret'])
                accountDb.close()
                accountPunishmentDb.close()
                return None
        accountDb.close()
        accountPunishmentDb.close()
        return None

    @staticmethod
    def refresh_token(refresh_token: str) -> dict:
        """
        Créer un nouveau token JWT à partir du refresh token
        """
        user = RefreshToken.decodeRefreshToken(refresh_token)
        if user != None:
            jwt = JWT.signJWT(user['uuid'])
            refresh_token = RefreshToken.signRefreshToken(jwt)
            return {"access_token": jwt, "refresh_token": refresh_token}
        else:
            return None