import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    return pymysql.connect(host=os.getenv('MYSQL_HOST'),
                           port=int(os.getenv('MYSQL_PORT')),
                           user=os.getenv('MYSQL_USER'),
                           password=os.getenv('MYSQL_PASSWORD'),
                           database=os.getenv('MYSQL_DATABASE'),
                           cursorclass=pymysql.cursors.DictCursor)