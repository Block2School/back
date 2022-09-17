import json
from typing import Dict
from database.Articles import articlesDb
from datetime import datetime
import requests
import os
import base64

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

    @staticmethod
    def create_markdown(filename: str, content: str) -> Dict[bool, str]:
        headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        data = {
            "message": f"Adding {filename}.md to the repository",
            "content": str(base64.b64encode(content.encode('ascii')).decode("ascii"))
        }
        try:
            r = requests.put(f'https://api.github.com/repos/Block2School/Blog/contents/{filename}.md', data=json.dumps(data), headers=headers)
            r = r.json()
            print(f'Github response: {r}')
            return {'success': True, 'url': r['content']['download_url']}
        except Exception as e:
            print(f'error: {e}')
            return {'success': False}

    @staticmethod
    def get_markdown_list() -> Dict[bool, list]:
        headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        try:
            r = requests.get('https://api.github.com/repos/Block2School/Blog/contents', headers=headers)
            r = r.json()
            markdowns = []
            for i in range(0, len(r)):
                if r[i]['name'].endswith('.md'):
                    markdowns.append({'title': r[i]['name'].replace('.md', ''), 'markdown_url': r[i]['download_url']})
            return {'success': True, 'markdowns': markdowns}
        except Exception as e:
            print(f'error: {e}')
            return {'success': False, 'markdowns': []}