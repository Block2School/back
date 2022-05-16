from datetime import datetime
import uuid
from database.Account import accountDb
from services.utils.JWT import JWT
from services.utils.WalletHash import WalletHash
from database.AccountDetails import accountDetailDb
from database.AccountPunishment import accountPunishmentDb

class LoginService():
    @staticmethod
    def check_account(encrypted_wallet: str) -> list:
        wallet_hash = WalletHash.wallet_hash(encrypted_wallet)
        user_uuid = accountDb.login(wallet_hash)
        if len(user_uuid) != 0:
            return [wallet_hash, user_uuid[0][0]]
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
    def login(user_uuid: str) -> str:
        jwt = JWT.signJWT(user_uuid)
        return jwt

    @staticmethod
    def is_banned(user_uuid: str) -> dict:
        account = accountDb.fetch(user_uuid)
        if account[0][1]:
            bans = accountPunishmentDb.fetch(user_uuid)
            if len(bans) > 0:
                ban = bans[-1]
                if ban[2] != None:
                    if datetime.now() > ban[2]:
                        accountDb.update(user_uuid, False)
                        return None
                if not ban[3]:
                    return {"reason": ban[0], "expires": datetime.timestamp(ban[2]) if ban[2] else -1}
                else:
                    accountDb.update(user_uuid, False)
                    return None
            else:
                accountDb.update(user_uuid, False)
                return None
        return None