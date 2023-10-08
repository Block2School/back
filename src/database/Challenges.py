import pymysql
from services.utils.Log import Log


class Challenges():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def __log_error(self, e: Exception, function: str) -> None:
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("challenges table", function, function, message)

    def insert(
        self,
        inputs: str, # json
        answers: str, # json
        markdown_url: str,
        start_code: str,
        points: int,
        title: str = "",
        language: str = "python"
    ) -> bool:
        print(inputs)
        prepare = "INSERT INTO `challenges` (`inputs`, `answers`, `markdown_url`, `start_code`, `points`, `title`, `language`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (inputs, answers, markdown_url, start_code, points, title, language))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            print(e)
            return False
        return True

    def fetch(self, id: int) -> dict:
        prepare = "SELECT `id`, `inputs`, `answers`, `markdown_url`, `start_code`, `points`, `title`, `language` FROM `challenges` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None

    def fetch_all(self) -> list:
        prepare = "SELECT `id`, `inputs`, `answers`, `markdown_url`, `start_code`, `points`, `title`, `language` FROM `challenges`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_all")
            return None

    def fetch_random(self) -> dict:
        prepare = "SELECT `id`, `inputs`, `answers`, `markdown_url`, `start_code`, `points`, `title`, `language` FROM `challenges` ORDER BY RAND() LIMIT 1"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_random")
            return None

    def close(self) -> None:
        self.db.close()