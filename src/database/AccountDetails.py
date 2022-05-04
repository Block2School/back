from database.Database import db

class AccountDetails():
    def __init__(self, db):
        self.db = db

    def insert(self, uuid: str, wallet: str) -> bool:
        prepare = self.db.prepare('INSERT INTO account_details (uuid, wallet_address, username) VALUES ($1, $2, $3)')
        result = prepare(uuid, wallet, wallet)
        print(result)
        return len(result) == 2 and result[1] > 0

    def fetch(self, uuid: str) -> list:
        prepare = self.db.prepare('SELECT wallet_address, username, email FROM account_details WHERE uuid = $1')
        result = prepare(uuid)
        return result

    def update(self, uuid: str, username: str = None, email: str = None) -> list:
        if username != None and email != None:
            prepare = self.db.prepare('UPDATE account_details SET username = $1, email = $2 WHERE uuid = $3')
            result = prepare(username, email, uuid)
            return result
        elif username != None:
            prepare = self.db.prepare('UPDATE account_details SET username = $1 WHERE uuid = $2')
            result = prepare(username, uuid)
            return result
        elif email != None:
            prepare = self.db.prepare('UPDATE account_details SET email = $1 WHERE uuid = $2')
            prepare(email, uuid)
            return result
        else:
            return None

accountDetailDb = AccountDetails(db)
