import pymysql
class AccountDatabase():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def insert(self, uuid: str, wallet_address: str) -> bool:
        prepare = "INSERT INTO `account` (`uuid`, `wallet_address`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid, wallet_address))
            self.db.commit()
        except:
            return False
        return True

    def login(self, wallet_address: str) -> dict:
        prepare = "SELECT `uuid`, `discord_tag`, `qr_secret` FROM `account` WHERE `wallet_address` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (wallet_address))
                result = cursor.fetchone()
            return result
        except:
            return None

    def fetch(self, uuid: str) -> dict:
        prepare = "SELECT `wallet_address`, `is_banned`, `discord_tag`, `discord_token`, `authenticator_revoke_list`, `qr_secret`, `points` FROM `account` WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (uuid))
                result = cursor.fetchone()
            return result
        except:
            return None

    def fetchall(self) -> list:
        prepare = "SELECT `uuid`, `wallet_address`, `is_banned`, `discord_tag`, `points` FROM `account`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
            return result
        except:
            return None

    def add_revoke_word_list(self, uuid: str, revoke_list: str) -> dict:
        prepare = "UPDATE `account` SET `authenticator_revoke_list` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (revoke_list, uuid))
            self.db.commit()
            return {'uuid': uuid, 'revoke_word_list': revoke_list}
        except:
            return None

    def update(self, uuid: str, is_banned: bool, discord_tag: str, discord_token: str, qr_secret: str) -> dict:
        prepare = "UPDATE `account` SET `is_banned` = %r, `discord_tag` = %s, `discord_token` = %s, `qr_secret` = %s  WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (is_banned, discord_tag, discord_token, qr_secret, uuid))
            self.db.commit()
            return {'uuid': uuid, 'is_banned': is_banned}
        except:
            return None

    def update_points(self, uuid: str, points: int) -> dict:
        prepare = "UPDATE `account` SET `points` = %s WHERE `uuid` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (points, uuid))
            self.db.commit()
            return {"uuid": uuid, 'points': points}
        except:
            return None

    def close(self):
        self.db.close()