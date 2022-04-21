import postgresql
from database.Database import db

class AccountDatabase():
    def __init__(self, db) -> None:
        self.db = db

    def insert(self, uuid: str, wallet_address: str) -> bool:
        prepare = self.db.prepare('INSERT INTO account (uuid, wallet_address) VALUES ($1, $2)')
        result = prepare(uuid, wallet_address)
        return len(result) == 2 and result[1] > 0

    def fetch(self, wallet_address: str) -> list:
        prepare = self.db.prepare("SELECT uuid FROM account WHERE wallet_address = $1")
        result = prepare(wallet_address)
        return result

    def update(self, uuid: str, is_banned: bool) -> list:
        prepare = self.db.prepare("UPDATE account SET is_banned = $1 WHERE uuid = $2")
        result = prepare(is_banned, uuid)
        return result

accountDb = AccountDatabase(db)