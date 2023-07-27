import pymysql
from services.utils.Log import Log

class Articles():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("articles table", function, function, message)

    def insert(self, title: str, markdown_url: str, short_description: str, author: str) -> bool:
        prepare = "INSERT INTO `articles` (`title`, `markdown_url`, `short_description`, `author`) VALUES (%s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, short_description, author))
            self.db.commit()
            return True
        except Exception as e:
            self.__log_error(e, "insert")
            return False

    def fetch(self, id: int) -> dict:
        prepare = "SELECT `id`, `title`, `markdown_url` AS `markdownUrl`, `short_description` AS `shortDescription`, `author`, `created_at` AS `publicationDate`, `updated_at` AS `editDate` FROM `articles` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def fetchall(self) -> list:
        prepare = "SELECT `id`, `title`, `markdown_url` AS `markdownUrl`, `short_description` AS `shortDescription`, `author`, `created_at` AS `publicationDate`, `updated_at` AS `editDate` FROM `articles`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetchall")
            return None
        return result

    def update(self, id: int, title: str, markdown_url: str, short_description: str) -> bool:
        prepare = "UPDATE `articles` SET `title` = %s, `markdown_url` = %s, `short_description` = %s WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, short_description, id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return False
        return True

    def remove(self, id: int) -> bool:
        prepare = "DELETE FROM `articles` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "remove")
            return False
        return True

    def close(self):
        self.db.close()
