import pymysql
from database.Database import db

class UserTutorialScore():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, uuid: str, tutorial_id: int, language: str, characters: int, lines: int) -> bool:
        prepare = "INSERT INTO `user_tutorial_score` (`uuid`, `tutorial_id`, `language`, `characters`, `lines`) VALUES (%s, %s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id, language, characters, lines))
            self.db.commit()
        except Exception as e:
            print("e => ",e)
            return False
        return

    def update(self, uuid: str, tutorial_id: int, language: str, characters: int = -1, lines: int = -1) -> dict:
        if characters != -1:
            prepare = "UPDATE `user_tutorial_score` SET `characters` = %s WHERE `uuid` = %s AND `tutorial_id` = %s AND `language` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (characters, uuid, tutorial_id, language))
                self.db.commit()
            except:
                return None
            return {'uuid': uuid, 'tutorial_id': tutorial_id, 'language': language, 'characters': characters}
        elif lines != -1:
            prepare = "UPDATE `user_tutorial_score` SET `lines` = %s WHERE `uuid` = %s AND `tutorial_id` = %s AND `language` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (lines, uuid, tutorial_id, language))
                self.db.commit()
            except:
                return None
            return {'uuid': uuid, 'tutorial_id': tutorial_id, 'language': language, 'lines': lines}

    def fetch(self, uuid: str, tutorial_id: int, language: str) -> dict:
        prepare = "SELECT `uuid`, `tutorial_id`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s AND `tutorial_id` = %s AND `language` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id, language))
                result = cursor.fetchone()
            return result
        except:
            return None

    def fetch_all_score_of_user(self, uuid: str) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
            return result
        except:
            return None

    def fetch_all_score_of_user_by_tutorial_id(self, uuid: str, tutorial_id: int) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
                result = cursor.fetchall()
            return result
        except:
            return None

    def fetch_all_score_of_tutorial(self, tutorial_id: int) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (tutorial_id))
                result = cursor.fetchall()
            return result
        except:
            return None

userTutorialScoreDb = UserTutorialScore(db)