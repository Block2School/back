from database.Database import db
import pymysql

class AccountDetails():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, uuid: str, wallet: str) -> bool:
        prepare = "INSERT INTO `account_details` (`uuid`, `wallet_address`, `username`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, wallet, wallet))
            self.db.commit()
        except:
            return False
        return True

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `wallet_address`, `username`, `email` FROM `account_details` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
                return result
        except:
            return None

    def update(self, uuid: str, username: str = None, email: str = None) -> dict:
        if username != None and email != None:
            prepare = "UPDATE `account_details` SET `username` = %s, `email` = %s WHERE `uuid` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (username, email, uuid))
                self.db.commit()
            except:
                return None
            return {"username": username, "email": email, "uuid": uuid}
        elif username != None:
            prepare = "UPDATE `account_details` SET `username` = %s WHERE `uuid` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (username, uuid))
                self.db.commit()
            except:
                return None
            return {"username": username, "uuid": uuid}
        elif email != None:
            prepare = "UPDATE `account_details` SET `email` = %s WHERE `uuid` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (email, uuid))
                self.db.commit()
            except:
                return None
            return {"email": email, "uuid": uuid}
        else:
            return None

accountDetailDb = AccountDetails(db)
