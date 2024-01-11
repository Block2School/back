import pymysql
from services.utils.Log import Log

class Paths():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def __log_error(self, e: Exception, function: str) -> None:
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("paths table", function, function, message)

    def insert(self, title: str) -> bool:
        prepare = "INSERT INTO `path` (`path`) VALUES (%s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch(self, id: int) -> dict:
        prepare = "SELECT * FROM `path` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def fetch_all(self) -> list:
        prepare = "SELECT * FROM `path`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_all")
            return None
        return result

    def update(self, id: int, title: str) -> dict:
        prepare = "UPDATE `path` SET `path` = %s WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return self.fetch(id)

    def delete(self, id: int) -> bool:
        prepare = "DELETE FROM `path` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "delete")
            return False
        return True

    def close(self) -> None:
        self.db.close()