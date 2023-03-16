import pymysql

class UserAccess():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, uuid: str, data: str, access: str) -> bool:
        prepare = "INSERT INTO `user_access` (`uuid`, `data`, `access`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, data, access))
            self.db.commit()
        except:
            return False
        return True

    def fetch(self, uuid: str, data: str) -> dict:
        prepare = "SELECT `uuid`, `data`, `access` FROM `user_access` WHERE `uuid` = %s AND `data` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, data))
                result = cursor.fetchone()
                return result
        except:
            return None

    def update(self, uuid: str, data: str, access: str) -> dict:
        prepare = "UPDATE `user_access` SET `access` = %s WHERE `uuid` = %s, `data` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (access, uuid, data))
            self.db.commit()
        except:
            return None
        return {"uuid": uuid, "data": data, "access": access}

    def update_all_user_access(self, uuid: str, access: str) -> bool:
        prepare = "UPDATE `user_access` SET `access` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (access, uuid))
            self.db.commit()
        except:
            return False
        return True

    def close(self):
        self.db.close()
