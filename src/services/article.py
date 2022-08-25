from database.Articles import articlesDb
from datetime import datetime

class ArticleService():
    @staticmethod
    def get_all_articles() -> list:
        articles = articlesDb.fetchall()
        for i in range(0, len(articles)):
            articles[i]['publicationDate'] = datetime.timestamp(articles[i]['publicationDate'])
            articles[i]['editDate'] = datetime.timestamp(articles[i]['editDate'])
        return articles

    @staticmethod
    def get_article(id: int) -> dict:
        article = articlesDb.fetch(id)
        article['publicationDate'] = datetime.timestamp(article['publicationDate'])
        article['editDate'] = datetime.timestamp(article['editDate'])
        return article

    @staticmethod
    def create_article(title: str, markdown_url: str, author: str, short_description: str) -> bool:
        success = articlesDb.insert(title, markdown_url, short_description, author)
        return success

    @staticmethod
    def update_article(id: int, title: str, markdown_url: str, short_description: str) -> bool:
        result = articlesDb.update(id, title, markdown_url, short_description)
        return result

    @staticmethod
    def delete_article(id: int) -> bool:
        result = articlesDb.remove(id)
        return result