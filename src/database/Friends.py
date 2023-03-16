import pymysql

class Friends():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def insert(self, uuid: str, uuid_friend: str, status: str) -> bool:
        prepare = "INSERT INTO `friends` (`uuid`, `friend_uuid`, `status`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend, status))
            self.db.commit()
        except:
            return False
        return True

    def update(self, uuid: str, uuid_friend: str, status: str) -> dict:
        prepare = "UPDATE `friends` SET `status` = %s WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (status, uuid, uuid_friend))
            self.db.commit()
            return {"uuid": uuid, "uuid_friend": uuid_friend, "status": status}
        except:
            return None

    def remove(self, uuid: str, uuid_friend: str) -> bool:
        prepare = "DELETE FROM `friends` WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend))
            self.db.commit()
        except:
            return False
        return True

    def fetch(self, uuid: str, uuid_friend: str) -> dict:
        prepare = "SELECT `uuid`, `friend_uuid`, `status` FROM `friends` WHERE `uuid` = %s AND `friend_uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, uuid_friend))
                result = cursor.fetchone()
        except:
            return None
        return result

    def fetchall(self, uuid: str) -> list:
        prepare = "SELECT `uuid`, `friend_uuid`, `status` FROM `friends` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchall()
        except:
            return None
        return result

    def close(self):
        self.db.close()
