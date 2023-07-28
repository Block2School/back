import pymysql
from services.utils.Log import Log

class Category():
    def __init__(self, db: pymysql.connect):
        self.db = db

    def __log_error(self, e: Exception, function: str):
        if len(e.args) == 2:
            _, message = e.args
        else:
            message = str(e.args[0])
        Log.error_log("category table", function, function, message)

    def fetch_all_categories(self) -> list:
        prepare = "SELECT * FROM `category`"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare)
                result = cursor.fetchall()
        except Exception as e:
            self.__log_error(e, "fetch_all_categories")
            return None
        return result

    def create_category(self, name: str, description: str, image_url: str) -> bool:
        prepare = "INSERT INTO `category` (`name`, `description`, `image_url`) VALUES (%s, %s, %s)"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name, description, image_url))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "create_category")
            return False
        return True

    def update_category(self, name: str, description: str, image_url: str) -> dict:
        prepare = "UPDATE `category` SET `description` = %s, `image_url` = %s WHERE `name` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (description, image_url, name))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "update_category")
            return None
        return {"name": name, "description": description, "image_url": image_url}

    def delete_category(self, name: str) -> bool:
        prepare = "DELETE FROM `category` WHERE `name` = %s"
        try:
            with self.db.cursor() as cursor:
                cursor.execute(prepare, (name))
            self.db.commit()
        except Exception as e:
            self.__log_error(e, "delete_category")
            return False
        return True

    def close(self):
        self.db.close()
