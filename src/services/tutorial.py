from datetime import datetime
import json
from database.Tutorials import Tutorials
from database.Category import Category
from database.AccountTutorialCompletion import AccountTutorialCompletion
from database.UserTutorialScore import UserTutorialScore
from database.Database import Database
from database.Account import AccountDatabase
from typing import Dict
import os
import requests
import base64

class TutorialService():
    @staticmethod
    def get_all_tutorials() -> list:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorials = tutorialDb.fetch_all()
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] #if tutorial['should_be_check'] else None
                , 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled']})
        else:
            tutorialDb.close()
            return []
        tutorialDb.close()
        return tutorial_list

    @staticmethod
    def get_tutorial(id: int) -> dict:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorial = tutorialDb.fetch(id)
        if tutorial != None:
            data = tutorial
            return {'id': data['id'], 'title': data['title'], 'markdownUrl': data['markdown_url'], 'category': data['category'], 'answer': data['answer'] #if data['should_be_check'] else None
            , 'startCode': data['start_code'], 'shouldBeCheck': data['should_be_check'], 'enabled': data['enabled']}
        tutorialDb.close()
        return None

    @staticmethod
    def create_tutorial(title: str, markdownUrl: str, startCode: str, category: str, answer: str, shouldBeCheck: bool, input: str) -> bool:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        result = tutorialDb.insert(title, markdownUrl, category, answer, startCode, shouldBeCheck, input)
        tutorialDb.close()
        return result

    @staticmethod
    def get_all_tutorials_by_category(category: str) -> list:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorials = tutorialDb.fetch_by_category(category)
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] if tutorial['should_be_check'] else None, 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled']})
        else:
            tutorialDb.close()
            return []
        tutorialDb.close()
        return tutorial_list

    @staticmethod
    def update_tutorial(id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str) -> bool:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        result = tutorialDb.update(id, title, markdown_url, category, answer, start_code, should_be_check, input)
        tutorialDb.close()
        return result

    @staticmethod
    def toggle_tutorial(id: int, updated: bool) -> dict:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        result = tutorialDb.update_enabled(id, updated)
        if result:
            tutorialDb.close()
            return {'id': id, 'enabled': updated}
        tutorialDb.close()
        return None

    @staticmethod
    def get_all_categories() -> list:
        categoryDb: Category = Database.get_table("category")
        result = categoryDb.fetch_all_categories()
        returning = []
        for cat_list in result:
            returning.append({'name': cat_list['name'], 'description': cat_list['description'], 'image': cat_list['image_url']})
        categoryDb.close()
        return returning

    @staticmethod
    def create_category(name: str, description: str, image_url: str) -> bool:
        categoryDb: Category = Database.get_table("category")
        result = categoryDb.create_category(name, description, image_url)
        categoryDb.close()
        return result

    @staticmethod
    def update_category(name: str, description: str, image_url: str) -> bool:
        categoryDb: Category = Database.get_table("category")
        result = categoryDb.update_category(name, description, image_url)
        categoryDb.close()
        return result

    @staticmethod
    def delete_category(name: str) -> bool:
        categoryDb: Category = Database.get_table("category")
        result = categoryDb.delete_category(name)
        categoryDb.close()
        return result

    @staticmethod
    def validate_tutorial(uuid: str, tutorial_id: int) -> int:
        accountTutorialCompletionDb: AccountTutorialCompletion = Database.get_table("account_tutorial_completion")
        total_completions = accountTutorialCompletionDb.fetch_tutorial(uuid, tutorial_id)
        if total_completions == None:
            total_completions = 1
        else:
            total_completions = total_completions['total_completions']
            total_completions += 1

        if total_completions == 1:
            result = accountTutorialCompletionDb.insert(uuid, tutorial_id)
            if result:
                accountTutorialCompletionDb.close()
                return 1
            accountTutorialCompletionDb.close()
            return 0
        else:
            result = accountTutorialCompletionDb.update(uuid, tutorial_id, total_completions)
            accountTutorialCompletionDb.close()
            return result['total_completions']

    @staticmethod
    def get_scoreboard_tutorial_id(tutorial_id: int) -> list:
        accountTutorialCompletionDb: AccountTutorialCompletion = Database.get_table("account_tutorial_completion")
        userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
        scoreboard_tutorial_list = userTutorialScoreDb.fetch_all_score_of_tutorial(tutorial_id)
        scoreboard_tutorial_list.sort(key=lambda obj: obj['characters'], reverse=True)

        for i in range(0, len(scoreboard_tutorial_list)):
            uuid = scoreboard_tutorial_list[i].get('uuid')
            tmp = accountTutorialCompletionDb.fetch_tutorial(uuid, tutorial_id)
            scoreboard_tutorial_list[i]['total_completions'] = tmp.get('total_completions')
        accountTutorialCompletionDb.close()
        userTutorialScoreDb.close()
        return scoreboard_tutorial_list

    @staticmethod
    def get_percentage_tutorial_id(tutorial_id: int) -> float:
        accountTutorialCompletionDb: AccountTutorialCompletion = Database.get_table("account_tutorial_completion")
        accountDb: AccountDatabase = Database.get_table("account")
        total_completions = len(accountTutorialCompletionDb.fetch_by_tutorial_id(tutorial_id))
        total_users = len(accountDb.fetchall())
        accountTutorialCompletionDb.close()
        accountDb.close()
        return (total_completions / total_users) * 100

    @staticmethod
    def get_user_scoreboard(uuid: str) -> list:
        userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
        scores = userTutorialScoreDb.fetch_all_score_of_user(uuid)
        userTutorialScoreDb.close()
        return scores #call FastAPI fetch scoreboard

    @staticmethod
    def get_user_success(uuid: str) -> list:
        accountTutorialCompletionDb: AccountTutorialCompletion = Database.get_table("account_tutorial_completion")
        success = accountTutorialCompletionDb.fetch_all_tutorials(uuid)
        for i in range(0, len(success)):
            success[i]['last_completion'] = datetime.timestamp(success[i]['last_completion'])
        accountTutorialCompletionDb.close()
        return success

    @staticmethod
    def get_total_number_tutorials() -> int:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorials = tutorialDb.fetch_all()
        tutorialDb.close()
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