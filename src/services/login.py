from datetime import datetime
import uuid
from database.Account import accountDb
from services.utils.JWT import JWT, RefreshToken
from services.utils.WalletHash import WalletHash
from database.AccountDetails import accountDetailDb
from database.AccountPunishment import accountPunishmentDb

class LoginService():
    @staticmethod
    def check_account(encrypted_wallet: str) -> list:
        wallet_hash = WalletHash.wallet_hash(encrypted_wallet)
        result = accountDb.login(wallet_hash)
        if result != None:
            return [wallet_hash, result['uuid'], result['discord_tag']]
        else:
            return [wallet_hash]

    @staticmethod
    def register(wallet_hash: str, wallet: str) -> str:
        user_uuid = uuid.uuid4()
        if accountDb.insert(str(user_uuid), wallet_hash):
            accountDetailDb.insert(str(user_uuid), wallet)
            jwt = JWT.signJWT(str(user_uuid))
            return jwt
        return None

    @staticmethod
    def login(user_uuid: str, discord_token: str = None) -> str:
        if discord_token == None:
            jwt = JWT.signJWT(user_uuid)
        else:
            account = accountDb.fetch(user_uuid)
            try:
                if account['discord_token'] == int(discord_token):
                    accountDb.update(user_uuid, account['is_banned'], account['discord_tag'], None)
                    jwt = JWT.signJWT(user_uuid)
                else:
                    return None
            except:
                return None
        return jwt

    @staticmethod
    def create_refresh_token(access_token: str) -> str:
        refresh_token = RefreshToken.signRefreshToken(access_token)
        return refresh_token

    @staticmethod
    def is_banned(user_uuid: str) -> dict:
        account = accountDb.fetch(user_uuid)
        if account == None:
            return None
        if account['is_banned']:
            bans = accountPunishmentDb.fetch(user_uuid)
            if len(bans) > 0:
                ban = bans[-1]
                if ban['expires'] != None:
                    if datetime.now() > ban['expires']:
                        accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'])
                        return None
                if not ban['is_revoked']:
                    return {"reason": ban['reason'], "expires": datetime.timestamp(ban['expires']) if ban['expires'] else -1}
                else:
                    accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'])
                    return None
            else:
                accountDb.update(user_uuid, False, account['discord_tag'], account['discord_token'])
                return None
        return None

    @staticmethod
    def refresh_token(refresh_token: str) -> dict:
        user = RefreshToken.decodeRefreshToken(refresh_token)
        if user != None:
            jwt = JWT.signJWT(user['uuid'])
            refresh_token = RefreshToken.signRefreshToken(jwt)
            return {"access_token": jwt, "refresh_token": refresh_token}
        else:
            return None