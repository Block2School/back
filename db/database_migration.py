import os
from dotenv import load_dotenv, set_key, find_dotenv
from database import get_database
import pymysql

dotenv_file = find_dotenv()
load_dotenv()

version = int(os.getenv('DB_VERSION')) if os.getenv('DB_VERSION') != None else -1
connection = get_database()

print("Database version " + str(version))

fakeFiles = []
files = [f for f in os.listdir('./db/') if os.path.isfile(os.path.join('./db/', f))]
for f in files:
    if f.split('.')[-1] != 'sql':
        fakeFiles.append(f)
for f in fakeFiles:
    del files[files.index(f)]
files = sorted(files, key=lambda x : int(x.split('_')[0]))
high_version = version

for f in files:
    try:
        ver = int(f.split('_')[0])
    except:
        continue
    if ver > version:
        sql_file = open('./db/' + f, 'r', encoding='utf-8')
        text = sql_file.read()
        sql_file.close()
        sql_executions = text.split(';')
        del sql_executions[-1]
        with connection.cursor() as cursor:
            for i in sql_executions:
                cursor.execute(i + ";")
        connection.commit()
        if ver > high_version:
            high_version = ver

if version < high_version:
    print("Finished database migration, now version " + str(high_version))
else:
    print("Database is already up to date")

set_key(dotenv_file, "DB_VERSION", str(high_version))
