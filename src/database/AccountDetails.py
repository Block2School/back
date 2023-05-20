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

    def fetch_privacy(self, name: str) -> dict:
        prepare = "SELECT `uuid`, `private` FROM `account_details` WHERE username = %s LIMIT 1"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name))
                result = cursor.fetchone()
                return result
        except:
            return None

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `wallet_address`, `username`, `email`, `description`, `twitter`, `youtube`, `birthdate`, `private` FROM `account_details` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
                return result
        except:
            return None

    def update(self, uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: datetime, private: str) -> dict:
        prepare = "UPDATE `account_details` SET `username` = %s, `email` = %s, `description` = %s, `twitter` = %s, `youtube` = %s, `birthdate` = %s, `private` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (username, email, description, twitter, youtube, birthdate, private, uuid))
            self.db.commit()
        except Exception as e:
            print(e)
            return None
        return {"uuid": uuid, "username": username, "email": email, "description": description, "twitter": twitter, "youtube": youtube, "private": private}

    def close(self):
        self.db.close()
