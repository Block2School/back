from datetime import datetime
import pymysql
from services.utils.Log import Log

class AccountPunishment():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("account_punishment table", function, function, message)

    def fetch(self, uuid: str) -> list:
        prepare = "SELECT `reason`, `banned_by`, `expires`, `is_revoked`, `revoked_by`, `revoke_reason` FROM `account_punishment` WHERE `uuid` = %s ORDER BY `created_at` ASC"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch")
            return None
        return result

    def insert(self, uuid: str, banned_by: str, reason: str, expires: datetime) -> bool:
        prepare = "INSERT INTO `account_punishment` (`uuid`, `banned_by`, `reason`, `expires`) VALUES (%s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, banned_by, reason, expires))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "insert")
            return False
        return True

    def update(self, uuid: str, revoked_by: str, revoke_reason: str) -> dict:
        prepare = "UPDATE `account_punishment` SET `is_revoked` = %r, `revoked_by` = %s, `revoke_reason` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (True, revoked_by, revoke_reason, uuid))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update")
            return None
        return {"is_revoked": True, "revoked_by": revoked_by, "revoke_reason": revoke_reason, "uuid": uuid}

    def close(self):
        self.db.close()
