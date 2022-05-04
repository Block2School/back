import uuid
from database.Account import accountDb
from services.utils.JWT import JWT
from services.utils.WalletHash import WalletHash
from database.AccountToken import accountTokenDb
from database.AccountDetails import accountDetailDb

class LoginService():
    @staticmethod
    def check_account(encrypted_wallet: str) -> list:
        wallet_hash = WalletHash.wallet_hash(encrypted_wallet)
        user_uuid = accountDb.fetch(wallet_hash)
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
            accountTokenDb.insert(str(user_uuid), jwt)
            return jwt
        return None

    @staticmethod
    def login(user_uuid: str) -> str:
        jwt = JWT.signJWT(user_uuid)
        accountTokenDb.update(user_uuid, jwt)
        return jwt