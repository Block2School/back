from database.Database import db

class AccountModeration():
    def __init__(self, db):
        self.db = db

    def insert(self, uuid: str, role: int) -> bool:
        prepare = self.db.prepare('INSERT INTO account_moderation (uuid, role) VALUES ($1, $2)')
        result = prepare(uuid, role)
        return len(result) > 0

    def fetch(self, uuid: str) -> list:
        prepare = self.db.prepare('SELECT role FROM account_moderation WHERE uuid = $1')
        result = prepare(uuid)
        return result

    def update(self, uuid: str, role: int) -> bool:
        prepare = self.db.prepare('UPDATE account_moderation SET role = $1 WHERE uuid = $2')
        result = prepare(role, uuid)
        return len(result) > 0

    def remove(self, uuid: str) -> bool:
        prepare = self.db.prepare('DELETE FROM account_moderation WHERE uuid = $1')
        result = prepare(uuid)
        return len(result) > 0

accountModerationDb = AccountModeration(db)