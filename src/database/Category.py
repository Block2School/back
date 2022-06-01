from database.Database import db

class Category():
    def __init__(self, db):
        self.db = db

    def fetch_all_categories(self) -> list:
        prepare = self.db.prepare('SELECT * FROM category')
        result = prepare()
        return result

    def create_category(self, name: str, description: str, image_url: str) -> bool:
        prepare = self.db.prepare('INSERT INTO category (name, description, image_url) VALUES ($1, $2, $3)')
        result = prepare(name, description, image_url)
        return len(result) > 0

    def update_category(self, name: str, description: str, image_url: str) -> bool:
        prepare = self.db.prepare('UPDATE category SET description = $1, image_url = $2 WHERE name = $3')
        result = prepare(description, image_url, name)
        return len(result) > 0

    def delete_category(self, name: str) -> bool:
        prepare = self.db.prepare('DELETE FROM category WHERE name = $1')
        result = prepare(name)
        return len(result) > 0

categoryDb = Category(db)