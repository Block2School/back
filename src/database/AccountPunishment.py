from datetime import datetime
from database.Database import db

class AccountPunishment():
    def __init__(self, db):
        self.db = db

    def fetch(self, uuid: str) -> list:
        prepare = self.db.prepare('SELECT reason, expires, is_revoked, revoked_by, revoke_reason FROM account_punishment WHERE uuid = $1')
        result = prepare(uuid)
        return result

    def insert(self, uuid: str, reason: str, expires: datetime) -> list:
        prepare = self.db.prepare('INSERT INTO account_punishment (uuid, reason, expires) VALUES ($1, $2, $3)')
        result = prepare(uuid, reason, expires)
        return result

    def update(self, uuid: str, revoked_by: str, revoke_reason: str) -> list:
        prepare = self.db.prepare('UPDATE account_punishment SET is_revoked = $1, revoked_by = $2, revoke_reason = $3 WHERE uuid = $4')
        result = prepare(True, revoked_by, revoke_reason, uuid)
        return result

accountPunishmentDb = AccountPunishment(db)