import pymysql
from services.utils.Log import Log

class UserTutorialScore():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("user_tutorial_score table", function, function, message)

    def insert(self, uuid: str, tutorial_id: int, language: str, characters: int, lines: int) -> bool:
        prepare = "INSERT INTO `user_tutorial_score` (`uuid`, `tutorial_id`, `total_completions`, `language`, `characters`, `lines`) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id, 1, language, characters, lines))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return

    def update(self, uuid: str, tutorial_id: int, total_completions:int, language: str, characters: int = -1, lines: int = -1) -> dict:
        print("enter")
        print("char => " + str(characters) + " || lines => " + str(lines))
        if characters != -1 and lines != -1:
            print(uuid, tutorial_id, language)
            prepare = "UPDATE `user_tutorial_score` SET `total_completions` = %s, `language` = %s, `characters` = %s, `lines` = %s WHERE `uuid` = %s AND `tutorial_id` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (total_completions, language, characters, lines, uuid, tutorial_id))
                self.db.commit()
            except Exception as e:
                self.__log_error(e, "update (characters & lines != -1)")
                return None
            return {'uuid': uuid, 'tutorial_id': tutorial_id, "total_completions": total_completions, 'language': language, 'characters': characters, 'lines': lines}
        elif characters != -1:
            print("char")
            prepare = "UPDATE `user_tutorial_score` SET `total_completions` = %s,`characters` = %s WHERE `uuid` = %s AND `tutorial_id` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (total_completions, characters, uuid, tutorial_id))
                self.db.commit()
            except Exception as e:
                self.__log_error(e, "update (characters != -1)")
                return None
            return {'uuid': uuid, 'tutorial_id': tutorial_id, "total_completions": total_completions, 'language': language, 'characters': characters}
        elif lines != -1:
            print("line")
            prepare = "UPDATE `user_tutorial_score` SET `total_completions` = %s, `lines` = %s WHERE `uuid` = %s AND `tutorial_id` = %s"
            try:
                with self.db.cursor() as cursor:
                    cursor.execute(prepare, (total_completions, lines, uuid, tutorial_id))
                self.db.commit()
            except Exception as e:
                self.__log_error(e, "update (lines != -1)")
                return None
            return {'uuid': uuid, 'tutorial_id': tutorial_id, "total_completions": total_completions, 'language': language, 'lines': lines}

    

    def fetch(self, uuid: str, tutorial_id: int, language : str) -> dict:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
                result = cursor.fetchone()
            return result
        except Exception as e:
            self.__log_error(e, "fetch")
            return None #un scoreboard pour un user et un langage en particulier
                        #enlever ce fetch plus d'ajout dans la db avec langage

    def fetch_all_score_of_user(self, uuid: str) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
            return result
        except Exception as e:
            self.__log_error(e, "fetch_all_score_of_user")
            return None # tous les scoreboard 

    def fetch_all_score_of_user_by_tutorial_id(self, uuid: str, tutorial_id: int) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
                result = cursor.fetchall()
            return result
        except Exception as e:
            self.__log_error(e, "fetch_all_score_of_user_by_tutorial_id")
            return None

    def fetch_all_score_of_tutorial(self, tutorial_id: int) -> list:
        prepare = "SELECT `uuid`, `tutorial_id`, `total_completions`, `language`, `characters`, `lines` FROM `user_tutorial_score` WHERE `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (tutorial_id))
                result = cursor.fetchall()
            return result
        except Exception as e:
            self.__log_error(e, "fetch_all_score_of_tutorial")
            return None

    def delete_score_of_user_on_tutorial(self, uuid:str, tutorial_id:int) -> list:
        prepare = "DELETE FROM `user_tutorial_score` WHERE `uuid` = %s AND `tutorial_id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, tutorial_id))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "delete_score_of_user_on_tutorial")
            return None
    
    def close(self):
        self.db.close()
