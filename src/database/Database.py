import os
from dotenv import load_dotenv
import pymysql
import pymysql.cursors
from database.Account import AccountDatabase
from database.AccountDetails import AccountDetails
from database.AccountModeration import AccountModeration
from database.AccountPunishment import AccountPunishment
from database.Articles import Articles
from database.Category import Category
from database.Faq import Faq
from database.Friends import Friends
from database.Tutorials import Tutorials
from database.UserAccess import UserAccess
from database.UserTutorialScore import UserTutorialScore

load_dotenv()

tables = {
    "account": AccountDatabase,
    "account_details": AccountDetails,
    "account_moderation": AccountModeration,
    "account_punishment": AccountPunishment,
    "articles": Articles,
    "category": Category,
    "faq": Faq,
    "friends": Friends,
    "tutorials": Tutorials,
    "user_access": UserAccess,
    "user_tutorial_score": UserTutorialScore
}

class Database():
    @staticmethod
    def get_table(table_name: str):
        if tables.get(table_name):
            db = pymysql.connect(host=os.getenv('MYSQL_HOST'),
                        port=int(os.getenv('MYSQL_PORT')),
                        user=os.getenv('MYSQL_USER'),
                        password=os.getenv('MYSQL_PASSWORD'),
                        database=os.getenv('MYSQL_DATABASE'),
                        cursorclass=pymysql.cursors.DictCursor)
            return tables[table_name](db)