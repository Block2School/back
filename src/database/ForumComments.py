import pymysql
from services.utils.Log import Log

class ForumComments():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("forum posts table", function, function, message)

    def insert(self, post_id:str, author_uuid:str, text:str) -> bool:
        prepare = "INSERT INTO `comments` (`post_id`, `author_uuid`, `text`) VALUES (%s, %s, %s)"
        print("STARTING INSERT FORUM Comments")
        try:
            with self.db.cursor() as cursor:
                print("HERE")
                cursor.execute(prepare, (post_id, author_uuid, text))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            print("ERROR", e)
            return False
        return True

    def fetch(self, post_id: int) -> dict:
        prepare = "SELECT * FROM `comments` WHERE `post_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (post_id))
                result = cursor.fetchall()
                print("RESULT FETCH DB", result)
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def fetch_all(self) -> list:
        prepare = "SELECT * FROM `forumPosts`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_all")
            return None
        return result

    def fetch_by_category(self, category: str) -> list:
        prepare = "SELECT * FROM `forumPosts` WHERE `category` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (category))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_by_category")
            return None
        return result

    def update(self, id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str, points: int, default_language: str, image: str, short_description: str, estimated_time: str) -> dict:
        prepare = "UPDATE `forumPosts` SET `title` = %s, `markdown_url` = %s, `category` = %s, `answer` = %s, `start_code` = %s, `should_be_check` = %r, `input` = %s, `points` = %s, `default_language` = %s, `image` = %s, `short_description` = %s, `estimated_time` = %s WHERE `id` = %s"
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
        prepare = "DELETE FROM `forumPosts` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "remove")
            return False
        return True

    def fetch_by_path(self, path: str) -> list:
        prepare = "SELECT * FROM `tutorials` WHERE `path` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (path))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_by_path")
            return None
        return result

    def get_total_nb_of_tutorials(self) -> int:
        prepare = "SELECT COUNT(*) AS total FROM `tutorials`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchone()
        except Exception as e:
            self.__log_error(e, "get_total_nb_of_tutorials")
            return None
        return result["total"]

    def close(self):
        self.db.close()
