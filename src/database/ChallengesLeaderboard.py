import pymysql
from services.utils.Log import Log


class ChallengesLeaderboard():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("challenges_leaderboard table", function, function, message)

    def insert(
        self,
        user_uuid: str,
    ) -> bool:
        prepare = "INSERT INTO `challenges_leaderboard` (`user_uuid`) VALUES (%s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (user_uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def fetch_all(self) -> list:
        prepare = "SELECT `user_uuid`, `points` FROM `challenges_leaderboard`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_all")
            return None

    def fetch_all_with_usernames(self) -> list:
        # get leaderboard with user_uuid, points and the username associated with the user_uuid
        prepare = "SELECT `challenges_leaderboard`.`user_uuid`, `challenges_leaderboard`.`points`, `account_details`.`username` FROM `challenges_leaderboard` INNER JOIN `account_details` ON `challenges_leaderboard`.`user_uuid` = `account_details`.`uuid`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.__log_error(e, "fetch_all_with_usernames")
            return None

    def fetch(self, user_uuid: str) -> dict:
        prepare = "SELECT `points` FROM `challenges_leaderboard` WHERE `user_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (user_uuid))
                result = cursor.fetchone()
                return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None

    def update(self, user_uuid: str, points: int) -> bool:
        prepare = "UPDATE `challenges_leaderboard` SET `points` = %s WHERE `user_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (points, user_uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return False
        return True

    def add_points(self, user_uuid: str, points: int) -> bool:
        prepare = "UPDATE `challenges_leaderboard` SET `points` = `points` + %s WHERE `user_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (points, user_uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "add_points")
            return False
        return True

    def close(self) -> None:
        self.db.close()