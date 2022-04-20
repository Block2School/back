import postgresql
from database.Database import db

class AccountToken():
    def __init__(self, db):
        self.db = db

    def insert(self, uuid: str, access_token: str) -> list:
        prepare = self.db.prepare("INSERT INTO account_token (uuid, access_token) VALUES ($1, $2)")
        result = prepare(uuid, access_token)
        return result

    def fetch_access_token(self, access_token: str) -> list:
        prepare = self.db.prepare("SELECT uuid FROM account_token WHERE access_token = $1")
        result = prepare(access_token)
        return result

    def update(self, uuid: str, access_token: str) -> list:
        prepare = self.db.prepare("UPDATE account_token SET access_token = $1 WHERE uuid = $2")
        result = prepare(access_token, uuid)
        return result

accountTokenDb = AccountToken(db)