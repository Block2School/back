import pymysql
from services.utils.Log import Log

class Friends():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("friends table", function, function, message)

    def insert(self, uuid: str, uuid_friend: str, status: str) -> bool:
        prepare = "INSERT INTO `friends` (`uuid`, `friend_uuid`, `status`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend, status))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def update(self, uuid: str, uuid_friend: str, status: str) -> dict:
        prepare = "UPDATE `friends` SET `status` = %s WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (status, uuid, uuid_friend))
            self.db.commit()
            return {"uuid": uuid, "uuid_friend": uuid_friend, "status": status}
        except Exception as e:
            self.__log_error(e, "update")
            return None

    def remove(self, uuid: str, uuid_friend: str) -> bool:
        prepare = "DELETE FROM `friends` WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "remove")
            return False
        return True

    def fetch(self, uuid: str, uuid_friend: str) -> dict:
        prepare = "SELECT `uuid`, `friend_uuid`, `status` FROM `friends` WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend))
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def fetchall(self, uuid: str) -> list:
        prepare = "SELECT `uuid`, `friend_uuid`, `status` FROM `friends` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetchall")
            return None
        return result

    def close(self):
        self.db.close()
