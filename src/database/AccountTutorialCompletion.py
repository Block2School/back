import pymysql

class AccountTutorialCompletion():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, uuid: str, tutorial_id: int) -> bool:
        prepare = "INSERT INTO `account_tutorial_completion` (`uuid`, `tutorial_id`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
            self.db.commit()
        except:
            return False
        return True

    def fetch_tutorial(self, uuid: str, tutorial_id: int) -> dict:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `updated_at` AS `last_completion` FROM `account_tutorial_completion` WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
                result = cursor.fetchone()
        except:
            return None
        return result #un scoreboard un user pour le tuto

    def fetch_all_tutorials(self, uuid: str) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `updated_at` AS `last_completion` FROM `account_tutorial_completion` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except:
            return None
        return result #tous les scoreboards d'un user pour tous les tutoriels

    def fetch_by_tutorial_id(self, tutorial_id: int) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions` FROM `account_tutorial_completion` WHERE `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (tutorial_id))
                result = cursor.fetchall()
        except:
            return None
        return result #les scoreboards tous les users pour un tutorial

    def update(self, uuid: str, tutorial_id: int, total_completions: int) -> dict:
        prepare = "UPDATE `account_tutorial_completion` SET `total_completions` = %s WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (total_completions, uuid, tutorial_id))
            self.db.commit()
        except:
            return None
        return {"uuid": uuid, "tutorial_id": tutorial_id, "total_completions": total_completions}

    def close(self):
        self.db.close()
