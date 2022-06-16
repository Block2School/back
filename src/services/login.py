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
        result = accountDb.login(wallet_hash)
        if result != None:
            return [wallet_hash, result['uuid']]
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
        if account == None:
            return None
        if account['is_banned']:
            bans = accountPunishmentDb.fetch(user_uuid)
            if len(bans) > 0:
                ban = bans[-1]
                if ban['expires'] != None:
                    if datetime.now() > ban['expires']:
                        accountDb.update(user_uuid, False)
                        return None
                if not ban['is_revoked']:
                    return {"reason": ban['reason'], "expires": datetime.timestamp(ban['expires']) if ban['expires'] else -1}
                else:
                    accountDb.update(user_uuid, False)
                    return None
            else:
                accountDb.update(user_uuid, False)
                return None
        return None