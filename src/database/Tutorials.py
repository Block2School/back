import pymysql
from services.utils.Log import Log

class Tutorials():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("tutorials table", function, function, message)

    def insert(self, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str, points: int, default_language: str, image: str, short_description: str, estimated_time: str) -> bool:
        prepare = "INSERT INTO `tutorials` (`title`, `markdown_url`, `category`, `answer`, `start_code`, `should_be_check`, `input`, `points`, `default_language`, `image`, `short_description`, `estimated_time`) VALUES (%s, %s, %s, %s, %s, %r, %s, %s, %s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, category, answer, start_code, should_be_check, input, points))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch(self, id: int) -> dict:
        prepare = "SELECT * FROM `tutorials` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def fetch_all(self) -> list:
        prepare = "SELECT * FROM `tutorials`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_all")
            return None
        return result

    def fetch_by_category(self, category: str) -> list:
        prepare = "SELECT * FROM `tutorials` WHERE `category` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (category))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_by_category")
            return None
        return result

    def update(self, id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str, points: int, default_language: str, image: str, short_description: str, estimated_time: str) -> dict:
        prepare = "UPDATE `tutorials` SET `title` = %s, `markdown_url` = %s, `category` = %s, `answer` = %s, `start_code` = %s, `should_be_check` = %r, `input` = %s, `points` = %s, `default_language` = %s, `image` = %s, `short_description` = %s, `estimated_time` = %s WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, category, answer, start_code, should_be_check, input, points, id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return {"id": id, "title": title, "markdown_url": markdown_url, "category": category, "answer": answer, "start_code": start_code, "should_be_check": should_be_check, "input": input, "points": points}

    def update_enabled(self, id: int, enabled: bool) -> dict:
        prepare = "UPDATE `tutorials` SET `enabled` = %r WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (enabled, id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update_enabled")
            return None
        return {"id": id, "enabled": enabled}

    def remove(self, id: int) -> bool:
        prepare = "DELETE FROM `tutorials` WHERE `id` = %s"
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
