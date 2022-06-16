from database.Database import db
import pymysql

class Category():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def fetch_all_categories(self) -> list:
        prepare = "SELECT * FROM `category`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except:
            return None
        return result

    def create_category(self, name: str, description: str, image_url: str) -> bool:
        prepare = "INSERT INTO `category` (`name`, `description`, `image_url`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name, description, image_url))
            self.db.commit()
        except:
            return False
        return True

    def update_category(self, name: str, description: str, image_url: str) -> dict:
        prepare = "UPDATE `category` SET `description` = %s, `image_url` = %s WHERE `name` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (description, image_url, name))
            self.db.commit()
        except:
            return None
        return {"name": name, "description": description, "image_url": image_url}

    def delete_category(self, name: str) -> bool:
        prepare = "DELETE FROM `category` WHERE `name` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name))
            self.db.commit()
        except:
            return False
        return True

categoryDb = Category(db)