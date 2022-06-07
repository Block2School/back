import postgresql
from database.Database import db

class AccountTutorialCompletion():
    def __init__(self, db):
        self.db = db

    def insert(self, uuid: str, tutorial_id: int) -> int:
        prepare = self.db.prepare('INSERT INTO account_tutorial_completion (uuid, tutorial_id) VALUES ($1, $2)')
        try:
            result = prepare(uuid, tutorial_id)
        except:
            return -1
        return result[0][2]

    def fetch_tutorial(self, uuid: str, tutorial_id: int) -> list:
        prepare = self.db.prepare('SELECT uuid, tutorial_id, total_completions, updated_at AS last_completion FROM account_tutorial_completion WHERE uuid = $1 AND tutorial_id = $2')
        result = prepare(uuid, tutorial_id)
        return result

    def fetch_all_tutorials(self, uuid: str) -> list:
        prepare = self.db.prepare('SELECT uuid, tutorial_id, total_completions, updated_at AS last_completion FROM account_tutorial_completion WHERE uuid = $1')
        result = prepare(uuid)
        return result

    def update(self, uuid: str, tutorial_id: int, total_completions: int) -> int:
        prepare = self.db.prepare('UPDATE account_tutorial_completion SET total_completions = $1 WHERE uuid = $2 AND tutorial_id = $3')
        result = prepare(total_completions, uuid, tutorial_id)
        return result[0][2]

accountTutorialCompletionDb = AccountTutorialCompletion(db)