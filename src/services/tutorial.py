from database.Tutorials import tutorialDb

class TutorialService():
    @staticmethod
    def get_all_tutorials() -> list:
        tutorials = tutorialDb.fetch_all()
        tutorial_list = []
        if len(tutorials) > 0:
            for tutorial in tutorials:
                tutorial_list.append({'id': tutorial[0], 'title': tutorial[1], 'markdownUrl': tutorial[2], 'category': tutorial[3], 'answer': tutorial[4] if tutorial[6] else None, 'startCode': tutorial[5], 'shouldBeCheck': tutorial[6], 'enabled': tutorial[9]})
        else:
            return []
        return tutorial_list

    @staticmethod
    def get_tutorial(id: int) -> dict:
        tutorial = tutorialDb.fetch(id)
        if len(tutorial) > 0:
            data = tutorial[0]
            return {'id': data[0], 'title': data[1], 'markdownUrl': data[2], 'category': data[3], 'answer': data[4] if data[6] else None, 'startCode': data[5], 'shouldBeCheck': data[6], 'enabled': data[9]}
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
                tutorial_list.append({'id': tutorial[0], 'title': tutorial[1], 'markdownUrl': tutorial[2], 'category': tutorial[3], 'answer': tutorial[4] if tutorial[6] else None, 'startCode': tutorial[5], 'shouldBeCheck': tutorial[6], 'enabled': tutorial[9]})
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
    def get_categories() -> list:
        category_list = []
        category_list.append({'description': 'Tutorials that are used for testing purposes.', 'image': 'https://www.lacase.mu/wp-content/uploads/2018/01/test1.jpg', 'name': 'Test'})
        category_list.append({'description': 'Tutorials that are the same as the ones in Test.', 'image': 'https://static-s.aa-cdn.net/img/ios/963076130/21feeed22ff00e4069eb1bb5df72fcd4?v=1', 'name': 'Tfou'})
        category_list.append({'description': 'Heho this is a description my friend.', 'image': 'https://scontent-cdt1-1.xx.fbcdn.net/v/t1.6435-9/37783620_247079442787852_7190952877701988352_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=cdDkMY70DMwAX9r-zW0&_nc_ht=scontent-cdt1-1.xx&oh=00_AT_tHX-x-72egZ0o4CfxwUz_wUA4-P8Ljvv0ugS5G4npZg&oe=62BA006E', 'name': 'Lol'})
        category_list.append({'description': 'Hi my name is John this is a description', 'image': 'https://i1.sndcdn.com/avatars-F0kzYliaHG2y9QMz-tCkkzw-t500x500.jpg', 'name': 'Zebi'})
        print(category_list, flush=True)
        return category_list