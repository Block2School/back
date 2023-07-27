import pymysql

class Faq():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def insert(self, question: str, answer: str) -> bool:
        prepare = "INSERT INTO `faq` (`question`, `answer`) VALUES (%s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (question, answer))
            self.db.commit()
        except:
            return False
        return True

    def remove(self, id: int) -> bool:
        prepare = "DELETE FROM `faq` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except:
            return False
        return True

    def fetchall(self) -> list:
        prepare = "SELECT `id`, `question`, `answer` FROM `faq`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except:
            return None
        return result

    def close(self):
        self.db.close()
