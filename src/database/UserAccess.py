import pymysql
from services.utils.Log import Log

class UserAccess():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("account table", function, function, message)

    def insert(self, uuid: str, data: str, access: str) -> bool:
        prepare = "INSERT INTO `user_access` (`uuid`, `data`, `access`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, data, access))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch(self, uuid: str, data: str) -> dict:
        prepare = "SELECT `uuid`, `data`, `access` FROM `user_access` WHERE `uuid` = %s AND `data` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, data))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None

    def update(self, uuid: str, data: str, access: str) -> dict:
        prepare = "UPDATE `user_access` SET `access` = %s WHERE `uuid` = %s, `data` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (access, uuid, data))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return {"uuid": uuid, "data": data, "access": access}

    def update_all_user_access(self, uuid: str, access: str) -> bool:
        prepare = "UPDATE `user_access` SET `access` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (access, uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update_all_user_access")
            return False
        return True

    def close(self):
        self.db.close()
