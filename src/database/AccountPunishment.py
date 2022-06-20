from datetime import datetime
from database.Database import db
import pymysql

class AccountPunishment():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def fetch(self, uuid: str) -> list:
        prepare = "SELECT `reason`, `banned_by`, `expires`, `is_revoked`, `revoked_by`, `revoke_reason` FROM `account_punishment` WHERE `uuid` = %s ORDER BY `created_at` ASC"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except:
            return None
        return result

    def insert(self, uuid: str, banned_by: str, reason: str, expires: datetime) -> bool:
        prepare = "INSERT INTO `account_punishment` (`uuid`, `banned_by`, `reason`, `expires`) VALUES (%s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, banned_by, reason, expires))
            self.db.commit()
        except:
            return False
        return True

    def update(self, uuid: str, revoked_by: str, revoke_reason: str) -> dict:
        prepare = "UPDATE `account_punishment` SET `is_revoked` = %r, `revoked_by` = %s, `revoke_reason` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (True, revoked_by, revoke_reason, uuid))
            self.db.commit()
        except:
            return None
        return {"is_revoked": True, "revoked_by": revoked_by, "revoke_reason": revoke_reason, "uuid": uuid}

accountPunishmentDb = AccountPunishment(db)