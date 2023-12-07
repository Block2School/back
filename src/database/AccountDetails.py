from datetime import datetime
import pymysql
from services.utils.Log import Log

class AccountDetails():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("account_details table", function, function, message)


    def insert(self, uuid: str, wallet: str) -> bool:
        prepare = "INSERT INTO `account_details` (`uuid`, `wallet_address`, `username`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, wallet, wallet))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch_privacy(self, name: str) -> dict:
        prepare = "SELECT `uuid`, `private` FROM `account_details` WHERE username = %s LIMIT 1"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_privacy")
            return None

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `wallet_address`, `username`, `email`, `description`, `twitter`, `youtube`, `birthdate`, `private` FROM `account_details` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None

    def update(self, uuid: str, username: str, email: str, description: str, twitter: str, youtube: str, birthdate: datetime, private: str) -> dict:
        prepare = "UPDATE `account_details` SET `username` = %s, `email` = %s, `description` = %s, `twitter` = %s, `youtube` = %s, `birthdate` = %s, `private` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (username, email, description, twitter, youtube, birthdate, private, uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return {"uuid": uuid, "username": username, "email": email, "description": description, "twitter": twitter, "youtube": youtube, "private": private}

    def search_user(self, username: str, start: int, offset: int) -> dict:
        prepare_count = "SELECT COUNT(*) AS total FROM account_details WHERE username LIKE %s"
        prepare = "SELECT uuid, username FROM account_details " \
                "WHERE username LIKE %s LIMIT %s OFFSET %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (f"%{username}%", offset, start))
                response = cursor.fetchall()
                cursor.execute(prepare_count, (f"%{username}%"))
                response_count = cursor.fetchone()
            self.db.commit()
            return response, response_count
        except Exception as e:
            self.__log_error(e, "search_user")
            return None

    def get_username(self, uuid: str) -> str:
        prepare = "SELECT username FROM account_details WHERE uuid = %s LIMIT 1"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                response = cursor.fetchone()
            self.db.commit()
            return response["username"]
        except Exception as e:
            self.__log_error(e, "get_username")
            return None

    def close(self):
        self.db.close()
