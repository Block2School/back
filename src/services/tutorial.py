from datetime import datetime
import json
from database.CompletedTutorials import CompletedTutorials
from database.Tutorials import Tutorials
from database.Category import Category
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
                , 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled'], 'points': tutorial['points'], 'inputs': tutorial['input'], 'default_language': tutorial['default_language'], 'image': tutorial['image'], 'short_description': tutorial['short_description'], 'estimated_time': tutorial['estimated_time']})
        else:
            tutorialDb.close()
            return []
        tutorialDb.close()
        return tutorial_list

    @staticmethod
    def get_all_tutorialsV2(uuid: str) -> list:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        completedTutorialDB: CompletedTutorials = Database.get_table("completed_tutorials")
        tutorials = tutorialDb.fetch_all()
        completed = completedTutorialDB.get_user_completed(uuid)
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] #if tutorial['should_be_check'] else None
                , 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'enabled': tutorial['enabled'], 'points': tutorial['points'], 'inputs': tutorial['input']
                , 'default_language': tutorial['default_language'], 'image': tutorial['image'], 'short_description': tutorial['short_description'], 'estimated_time': tutorial['estimated_time'], 'is_completed': False})
        else:
            tutorialDb.close()
            completedTutorialDB.close()
            return []

        if completed != None and len(completed) > 0:
            for compl in completed:
                for i in range(0, len(tutorial_list)):
                    if compl['tutorial_id'] == tutorial_list[i]['id']:
                        tutorial_list[i]['is_completed'] = True

        tutorialDb.close()
        completedTutorialDB.close()
        return tutorial_list

    @staticmethod
    def get_tutorial(id: int) -> dict:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorial = tutorialDb.fetch(id)
        if tutorial != None:
            data = tutorial
            return {'id': data['id'], 'title': data['title'], 'markdownUrl': data['markdown_url'], 'category': data['category'], 'answer': data['answer'] #if data['should_be_check'] else None
            , 'startCode': data['start_code'], 'shouldBeCheck': data['should_be_check'], 'enabled': data['enabled'], 'points': data['points'], 'inputs': data['input'], 'default_language': data['default_language'], 'image': data['image'], 'short_description': data['short_description'], 'estimated_time': data['estimated_time']}
        tutorialDb.close()
        return None

    @staticmethod
    def get_tutorialV2(id: int, uuid: str) -> dict:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        completedTutorialDB: CompletedTutorials = Database.get_table("completed_tutorials")
        tutorial = tutorialDb.fetch(id)
        if tutorial != None:
            data = tutorial
            completed = completedTutorialDB.get_user_completed(uuid)
            if completed != None and len(completed) > 0:
                for compl in completed:
                    if compl['tutorial_id'] == data['id']:
                        return {'id': data['id'], 'title': data['title'], 'markdownUrl': data['markdown_url'], 'category': data['category'], 'answer': data['answer'] #if data['should_be_check'] else None
                        , 'startCode': data['start_code'], 'shouldBeCheck': data['should_be_check'], 'enabled': data['enabled'], 'points': data['points'], 'inputs': data['input']
                        , 'default_language': data['default_language'], 'image': data['image'], 'short_description': data['short_description'], 'estimated_time': data['estimated_time'], 'is_completed': True}
            return {'id': data['id'], 'title': data['title'], 'markdownUrl': data['markdown_url'], 'category': data['category'], 'answer': data['answer'] #if data['should_be_check'] else None
            , 'startCode': data['start_code'], 'shouldBeCheck': data['should_be_check'], 'enabled': data['enabled'], 'points': data['points'], 'inputs': data['input']
            , 'default_language': data['default_language'], 'image': data['image'], 'short_description': data['short_description'], 'estimated_time': data['estimated_time'], 'is_completed': False}
        tutorialDb.close()
        completedTutorialDB.close()
        return None

    @staticmethod
    def create_tutorial(title: str, markdownUrl: str, startCode: str, category: str, answer: str, shouldBeCheck: bool, input: str, points: int) -> bool:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        result = tutorialDb.insert(title, markdownUrl, category, answer, startCode, shouldBeCheck, input, points)
        tutorialDb.close()
        return result

    @staticmethod
    def get_all_tutorials_by_category(category: str) -> list:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorials = tutorialDb.fetch_by_category(category)
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial['id'], 'title': tutorial['title'], 'markdownUrl': tutorial['markdown_url'], 'category': tutorial['category'], 'answer': tutorial['answer'] if tutorial['should_be_check'] else None, 'startCode': tutorial['start_code'], 'shouldBeCheck': tutorial['should_be_check'], 'points': tutorial['points'], 'enabled': tutorial['enabled']})
        else:
            tutorialDb.close()
            return []
        tutorialDb.close()
        return tutorial_list

    @staticmethod
    def update_tutorial(id: int, title: str, markdown_url: str, category: str, answer: str, start_code: str, should_be_check: bool, input: str, points: int) -> bool:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        result = tutorialDb.update(id, title, markdown_url, category, answer, start_code, should_be_check, input, points)
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
    def validate_tutorial(uuid: str, tutorial_id: int, language: str, characters: int, lines: int) -> int:
        userTutorialScoreDb : UserTutorialScore = Database().get_table("user_tutorial_score")
        total_completions = userTutorialScoreDb.fetch(uuid, tutorial_id, language)
        tutorial_completedDB: CompletedTutorials = Database().get_table("completed_tutorials")
        if total_completions == None:
            total_completions = 1
        else:
            total_completions = total_completions['total_completions']
            total_completions += 1

        tutorial_completedDB.insert(uuid, tutorial_id)

        if total_completions == 1:
            accountDb: AccountDatabase = Database().get_table("account")
            tutorialDb: Tutorials = Database().get_table("tutorials")
            tuto_details = tutorialDb.fetch(tutorial_id)
            result = userTutorialScoreDb.insert(uuid, tutorial_id, language, characters, lines)
            user = accountDb.fetch(uuid)
            accountDb.update_points(uuid, user['points'] + tuto_details['points'])
            accountDb.close()
            tutorialDb.close()
            if result:
                userTutorialScoreDb.close()
                return 1
            userTutorialScoreDb.close()
            return 0
        else:
            result = userTutorialScoreDb.update(uuid, tutorial_id, total_completions, language, characters, lines)
            userTutorialScoreDb.close()
            return result['total_completions']

    @staticmethod
    def get_scoreboard_tutorial_id(tutorial_id: int) -> list:
        userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
        scoreboard_tutorial_list = userTutorialScoreDb.fetch_all_score_of_tutorial(tutorial_id)
        scoreboard_tutorial_list.sort(key=lambda obj: obj['characters'], reverse=True)

        for i in range(0, len(scoreboard_tutorial_list)):
            uuid = scoreboard_tutorial_list[i].get('uuid')
            tmp = userTutorialScoreDb.fetch(uuid, tutorial_id)
            scoreboard_tutorial_list[i]['total_completions'] = tmp.get('total_completions')
        userTutorialScoreDb.close()
        return scoreboard_tutorial_list

    @staticmethod
    def get_percentage_tutorial_id(tutorial_id: int) -> float:
        userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
        accountDb: AccountDatabase = Database.get_table("account")
        total_completions = len(userTutorialScoreDb.fetch_all_score_of_tutorial(tutorial_id))
        total_users = len(accountDb.fetchall())
        userTutorialScoreDb.close()
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
        userTutorialScoreDb: UserTutorialScore = Database.get_table("user_tutorial_score")
        success = userTutorialScoreDb.fetch_all_score_of_user(uuid)
        userTutorialScoreDb.close()
        return success

    @staticmethod
    def get_total_number_tutorials() -> int:
        tutorialDb: Tutorials = Database.get_table("tutorials")
        tutorials = tutorialDb.fetch_all()
        tutorialDb.close()
        return len(tutorials)

    @staticmethod
    def get_user_completed_tutorials() -> list:
        pass

    @staticmethod
    def get_user_last_10_completed_tutorials() -> list:
        pass

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