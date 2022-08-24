import pymysql
from database.Database import db

class AccountDatabase():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def insert(self, uuid: str, wallet_address: str) -> bool:
        prepare = "INSERT INTO `account` (`uuid`, `wallet_address`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, wallet_address))
            self.db.commit()
        except:
            return False
        return True

    def login(self, wallet_address: str) -> dict:
        prepare = "SELECT `uuid` FROM `account` WHERE `wallet_address` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (wallet_address))
                result = cursor.fetchone()
            return result
        except:
            return None

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `wallet_address`, `is_banned` FROM `account` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
            return result
        except:
            return None

    def fetchall(self) -> list:
        prepare = "SELECT `wallet_address`, `is_banned` FROM `account`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
            return result
        except:
            return None

    def update(self, uuid: str, is_banned: bool) -> dict:
        prepare = "UPDATE `account` SET `is_banned` = %r WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (is_banned, uuid))
            self.db.commit()
            return {'uuid': uuid, 'is_banned': is_banned}
        except:
            return None

accountDb = AccountDatabase(db)