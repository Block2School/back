import pymysql
from services.utils.Log import Log

class AccountModeration():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("account_moderation table", function, function, message)


    def insert(self, uuid: str, role: int) -> bool:
        prepare = "INSERT INTO `account_moderation` (`uuid`, `role`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, role))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `role` FROM `account_moderation` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def update(self, uuid: str, role: int) -> dict:
        prepare = "UPDATE `account_moderation` SET `role` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (role, uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return {"role": role, "uuid": uuid}

    def remove(self, uuid: str) -> bool:
        prepare = "DELETE FROM `account_moderation` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "remove")
            return False
        return True

    def close(self):
        self.db.close()
