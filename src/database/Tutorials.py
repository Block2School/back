import postgresql
from database.Database import db

class Tutorials():
    def __init__(self, db):
        self.db = db

    def insert(self, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool) -> bool:
        prepare = self.db.prepare('INSERT INTO tutorials (title, markdown_url, category, answer, start_code, should_be_check) VALUES ($1, $2, $3, $4, $5, $6)')
        try:
            result = prepare(title, markdown_url, category, answer, start_code, should_be_check)
        except:
            return False
        return len(result) > 0

    def fetch(self, id: int) -> list:
        prepare = self.db.prepare('SELECT * FROM tutorials WHERE id = $1')
        result = prepare(id)
        return result

    def fetch_all(self) -> list:
        prepare = self.db.prepare('SELECT * from tutorials')
        result = prepare()
        return result

    def fetch_by_category(self, category: str) -> list:
        prepare = self.db.prepare('SELECT * from tutorials WHERE category = $1')
        result = prepare(category)
        return result

    def update(self, id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool) -> bool:
        prepare = self.db.prepare('UPDATE tutorials SET title = $1, markdown_url = $2, category = $3, answer = $4, start_code = $5, should_be_check = $6 WHERE id = $7')
        result = prepare(title, markdown_url, category, answer, start_code, should_be_check, id)
        return len(result) > 0

    def remove(self, id: int) -> bool:
        prepare = self.db.prepare('DELETE FROM tutorials WHERE id = $1')
        result = prepare(id)
        return len(result) > 0

tutorialDb = Tutorials(db)