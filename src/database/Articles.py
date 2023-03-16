import pymysql

class Articles():
    def __init__(self, db: pymysql.connect) -> None:
        self.db = db

    def insert(self, title: str, markdown_url: str, short_description: str, author: str) -> bool:
        prepare = "INSERT INTO `articles` (`title`, `markdown_url`, `short_description`, `author`) VALUES (%s, %s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, short_description, author))
            self.db.commit()
            return True
        except:
            return False

    def fetch(self, id: int) -> dict:
        prepare = "SELECT `id`, `title`, `markdown_url` AS `markdownUrl`, `short_description` AS `shortDescription`, `author`, `created_at` AS `publicationDate`, `updated_at` AS `editDate` FROM `articles` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
                result = cursor.fetchone()
        except:
            return None
        return result

    def fetchall(self) -> list:
        prepare = "SELECT `id`, `title`, `markdown_url` AS `markdownUrl`, `short_description` AS `shortDescription`, `author`, `created_at` AS `publicationDate`, `updated_at` AS `editDate` FROM `articles`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except:
            return None
        return result

    def update(self, id: int, title: str, markdown_url: str, short_description: str) -> bool:
        prepare = "UPDATE `articles` SET `title` = %s, `markdown_url` = %s, `short_description` = %s WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (title, markdown_url, short_description, id))
            self.db.commit()
        except:
            return False
        return True

    def remove(self, id: int) -> bool:
        prepare = "DELETE FROM `articles` WHERE `id` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (id))
            self.db.commit()
        except:
            return False
        return True

    def close(self):
        self.db.close()
