from datetime import datetime
import json
from database.Tutorials import tutorialDb
from database.Category import categoryDb
from database.AccountTutorialCompletion import accountTutorialCompletionDb
from database.UserTutorialScore import userTutorialScoreDb
from database.Account import accountDb
from typing import Dict
import os
import requests
import base64

class TutorialService():
    @staticmethod
    def get_all_tutorials() -> list:
        tutorials = tutorialDb.fetch_all()
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] if tutorial['should_be_check'] else None, 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled']})
        else:
            return []
        return tutorial_list

    @staticmethod
    def get_tutorial(id: int) -> dict:
        tutorial = tutorialDb.fetch(id)
        if tutorial != None:
            data = tutorial
            return {'id': data['id'], 'title': data['title'], 'markdownUrl': data['markdown_url'], 'category': data['category'], 'answer': data['answer'] if data['should_be_check'] else None, 'startCode': data['start_code'], 'shouldBeCheck': data['should_be_check'], 'enabled': data['enabled']}
        return None

    @staticmethod
    def create_tutorial(title: str, markdownUrl: str, startCode: str, category: str, answer: str, shouldBeCheck: bool) -> bool:
        result = tutorialDb.insert(title, markdownUrl, category, answer, startCode, shouldBeCheck)
        return result

    @staticmethod
    def get_all_tutorials_by_category(category: str) -> list:
        tutorials = tutorialDb.fetch_by_category(category)
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] if tutorial['should_be_check'] else None, 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled']})
        else:
            return []
        return tutorial_list

    @staticmethod
    def update_tutorial(id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool) -> bool:
        result = tutorialDb.update(id, title, markdown_url, category, answer, start_code, should_be_check)
        return result

    @staticmethod
    def toggle_tutorial(id: int, updated: bool) -> dict:
        result = tutorialDb.update_enabled(id, updated)
        if result:
            return {'id': id, 'enabled': updated}
        return None

    @staticmethod
    def get_all_categories() -> list:
        result = categoryDb.fetch_all_categories()
        returning = []
        for cat_list in result:
            returning.append({'name': cat_list['name'], 'description': cat_list['description'], 'image': cat_list['image_url']})
        return returning

    @staticmethod
    def create_category(name: str, description: str, image_url: str) -> bool:
        result = categoryDb.create_category(name, description, image_url)
        return result

    @staticmethod
    def update_category(name: str, description: str, image_url: str) -> bool:
        result = categoryDb.update_category(name, description, image_url)
        return result

    @staticmethod
    def delete_category(name: str) -> bool:
        result = categoryDb.delete_category(name)
        return result

    @staticmethod
    def validate_tutorial(uuid: str, tutorial_id: int) -> int:
        total_completions = accountTutorialCompletionDb.fetch_tutorial(uuid, tutorial_id)
        if total_completions == None:
            total_completions = 1
        else:
            total_completions = total_completions['total_completions']
            total_completions += 1

        if total_completions == 1:
            result = accountTutorialCompletionDb.insert(uuid, tutorial_id)
            if result:
                return 1
            return 0
        else:
            result = accountTutorialCompletionDb.update(uuid, tutorial_id, total_completions)
            return result['total_completions']

    @staticmethod
    def get_scoreboard_tutorial_id(tutorial_id: int) -> list:
        scoreboard_tutorial_list = userTutorialScoreDb.fetch_all_score_of_tutorial(tutorial_id)
        scoreboard_tutorial_list.sort(key=lambda obj: obj['characters'], reverse=True)

        for i in range(0, len(scoreboard_tutorial_list)):
            uuid = scoreboard_tutorial_list[i].get('uuid')
            tmp = accountTutorialCompletionDb.fetch_tutorial(uuid, tutorial_id)
            scoreboard_tutorial_list[i]['total_completions'] = tmp.get('total_completions')
        return scoreboard_tutorial_list

    @staticmethod
    def get_percentage_tutorial_id(tutorial_id: int) -> float:
        total_completions = len(accountTutorialCompletionDb.fetch_by_tutorial_id(tutorial_id))
        total_users = len(accountDb.fetchall())
        return (total_completions / total_users) * 100

    @staticmethod
    def get_user_scoreboard(uuid: str) -> list:
        scores = userTutorialScoreDb.fetch_all_score_of_user(uuid)
        return scores

    @staticmethod
    def get_user_success(uuid: str) -> list:
        success = accountTutorialCompletionDb.fetch_all_tutorials(uuid)
        for i in range(0, len(success)):
            success[i]['last_completion'] = datetime.timestamp(success[i]['last_completion'])
        return success

    @staticmethod
    def get_total_number_tutorials() -> int:
        tutorials = tutorialDb.fetch_all()
        return len(tutorials)

    @staticmethod
    def get_markdown_list() -> Dict[bool, list]:
        headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        try:
            r = requests.get('https://api.github.com/repos/Block2School/tutorials/contents/en', headers=headers)
            r = r.json()
            markdowns = []
            for i in range(0, len(r)):
                if r[i]['name'].endswith('.md'):
                    markdowns.append({'title': r[i]['name'].replace('.md', ''), 'markdown_url': r[i]['download_url']})
            return {'success': True, 'markdowns': markdowns}
        except Exception as e:
            print(f'error: {e}')
            return {'success': False, 'markdowns': []}

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
            r = requests.put(f'https://api.github.com/repos/Block2School/tutorials/contents/en/{filename}.md', data=json.dumps(data), headers=headers)
            r = r.json()
            print(f'Github response: {r}')
            return {'success': True, 'url': r['content']['download_url']}
        except Exception as e:
            print(f'error: {e}')
            return {'success': False}