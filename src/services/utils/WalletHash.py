import hashlib
from base64 import b64encode
import os
from dotenv import load_dotenv

load_dotenv()

class WalletHash():
    @staticmethod
    def wallet_hash(wallet_address: str) -> str:
        """
        Création du hash du wallet pour vérifier la connexion.
        """
        hash_wallet = hashlib.sha512(wallet_address.encode("ascii") + os.getenv('PASSWORD_HASH').encode("ascii")).digest()
        for _ in range(0, 100):
            hash_wallet = hashlib.sha512(hash_wallet + os.getenv('PASSWORD_SALT').encode('ascii')).digest()
        hash_wallet = b64encode(hash_wallet).decode('utf-8')
        return hash_wallet