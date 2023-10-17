from datetime import datetime
import pymysql
from services.utils.Log import Log


class ChallengesCompleted():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("challenges_completed table", function, function, message)

    def insert(
        self,
        uuid: str,
        challenge_id: int,
    ) -> bool:
        prepare = "INSERT INTO `challenges_completed` (`user_uuid`, `challenge_id`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, challenge_id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            print(e)
            return False
        return True

    def insert_if_never_completed(
        self,
        uuid: str,
        challenge_id: int
    ) -> bool:
        # check if the user has already completed the challenge before inserting if never completed add to db otherwise do nothing
        prepare = "SELECT `user_uuid` FROM `challenges_completed` WHERE `user_uuid` = %s AND `challenge_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, challenge_id))
                result = cursor.fetchone()
                if result is None:
                    return self.insert(uuid, challenge_id)
                else:
                    return True
        except Exception as e:
            self.__log_error(e, "insert_if_not_exists")
            return False

    def fetch_all_by_user(self, user_uuid: str) -> list:
        prepare = "SELECT `challenge_id`, `completed_at` FROM `challenges_completed` WHERE `user_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (user_uuid))
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_all_by_user")
            return None

    def fetch_all_by_challenge(self, challenge_id: int) -> list:
        prepare = "SELECT `user_uuid`, `completed_at` FROM `challenges_completed` WHERE `challenge_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (challenge_id))
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_all_by_challenge")
            return None

    def fetch(self, user_uuid: str, challenge_id: int) -> dict:
        prepare = "SELECT `completed_at` FROM `challenges_completed` WHERE `user_uuid` = %s AND `challenge_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (user_uuid, challenge_id))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None

    def close(self) -> None:
        self.db.close()
