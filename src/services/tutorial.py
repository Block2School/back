from database.Tutorials import tutorialDb
from database.Category import categoryDb
from database.AccountTutorialCompletion import accountTutorialCompletionDb

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