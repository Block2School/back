import pymysql
from services.utils.Log import Log

class CompletedTutorials():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("completed_tutorials table", function, function, message)

    def insert(self, uuid: str, tutorial_id: int):
        prepare = "INSERT INTO `completed_tutorials` (`user_id`, `tutorial_id`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
            self.db.commit()
        except Exception as e:
            # check if the error is because the tutorial is already completed
            if "Duplicate entry" in str(e.args[1]):
                return True
            self.__log_error(e, "insert")
            return False

    def get_user_completed(self, uuid: str) -> list:
        prepare = "SELECT `tutorial_id` FROM `completed_tutorials` WHERE `user_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "get_user_completed")
            return None
        return result

    def get_user_completedv2(self, uuid: str) -> list:
        # join with tutorials table to get the title of the tutorial
        prepare = "SELECT `completed_tutorials`.`tutorial_id`, `tutorials`.`title` FROM `completed_tutorials` JOIN `tutorials` ON `completed_tutorials`.`tutorial_id` = `tutorials`.`id` WHERE `user_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "get_user_completed")
            return None

    def get_user_last_10_completed_tutorials(self, uuid: str) -> list:
        prepare = "SELECT `tutorial_id` FROM `completed_tutorials` WHERE `user_id` = %s ORDER BY `completed_at` DESC LIMIT 10"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "get_user_last_10_completed_tutorials")
            return None
        return result

    def get_user_last_10_completed_tutorialsv2(self, uuid: str) -> list:
        prepare = "SELECT `completed_tutorials`.`tutorial_id`, `tutorials`.`title` FROM `completed_tutorials` JOIN `tutorials` ON `completed_tutorials`.`tutorial_id` = `tutorials`.`id` WHERE `user_id` = %s ORDER BY `completed_at` DESC LIMIT 10"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "get_user_last_10_completed_tutorials")
            return None
        return result