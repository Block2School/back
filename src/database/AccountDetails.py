from datetime import datetime
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
        prepare = "SELECT `wallet_address`, `username`, `email`, `description`, `twitter`, `youtube`, `birthdate` FROM `account_details` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
                return result
        except:
            return None

    def update(self, uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: datetime) -> dict:
        prepare = "UPDATE `account_details` SET `username` = %s, `email` = %s, `description` = %s, `twitter` = %s, `youtube` = %s, `birthdate` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (username, email, description, twitter, youtube, uuid, birthdate))
            self.db.commit()
        except:
            return None
        return {"uuid": uuid, "username": username, "email": email, "description": description, "twitter": twitter, "youtube": youtube}

    def close(self):
        self.db.close()
