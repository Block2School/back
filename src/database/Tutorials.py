import pymysql

class Tutorials():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def insert(self, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str) -> bool:
        prepare = "INSERT INTO `tutorials` (`title`, `markdown_url`, `category`, `answer`, `start_code`, `should_be_check`, `input`) VALUES (%s, %s, %s, %s, %s, %r, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, category, answer, start_code, should_be_check, input))
            self.db.commit()
        except:
            return False
        return True

    def fetch(self, id: int) -> dict:
        prepare = "SELECT * FROM `tutorials` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
        except:
            return None
        return result

    def fetch_all(self) -> list:
        prepare = "SELECT * FROM `tutorials`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except:
            return None
        return result

    def fetch_by_category(self, category: str) -> list:
        prepare = "SELECT * FROM `tutorials` WHERE `category` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (category))
                result = cursor.fetchall()
        except:
            return None
        return result

    def update(self, id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str) -> dict:
        prepare = "UPDATE `tutorials` SET `title` = %s, `markdown_url` = %s, `category` = %s, `answer` = %s, `start_code` = %s, `should_be_check` = %r, `input` = %s WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, category, answer, start_code, should_be_check, input, id))
            self.db.commit()
        except:
            return None
        return {"id": id, "title": title, "markdown_url": markdown_url, "category": category, "answer": answer, "start_code": start_code, "should_be_check": should_be_check, "input": input}

    def update_enabled(self, id: int, enabled: bool) -> dict:
        prepare = "UPDATE `tutorials` SET `enabled` = %r WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (enabled, id))
            self.db.commit()
        except:
            return None
        return {"id": id, "enabled": enabled}

    def remove(self, id: int) -> bool:
        prepare = "DELETE FROM `tutorials` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except:
            return False
        return True

    def close(self):
        self.db.close()
