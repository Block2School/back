import pymysql

class AccountModeration():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, uuid: str, role: int) -> bool:
        prepare = "INSERT INTO `account_moderation` (`uuid`, `role`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, role))
            self.db.commit()
        except:
            return False
        return True

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `role` FROM `account_moderation` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
        except:
            return None
        return result

    def update(self, uuid: str, role: int) -> dict:
        prepare = "UPDATE `account_moderation` SET `role` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (role, uuid))
            self.db.commit()
        except:
            return None
        return {"role": role, "uuid": uuid}

    def remove(self, uuid: str) -> bool:
        prepare = "DELETE FROM `account_moderation` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
            self.db.commit()
        except:
            return False
        return True

    def close(self):
        self.db.close()
