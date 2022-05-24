import os
from dotenv import load_dotenv, set_key, find_dotenv

dotenv_file = find_dotenv()
load_dotenv()

version = int(os.getenv('DB_VERSION'))

print("Database version " + str(version))

files = [f for f in os.listdir('./db/') if os.path.isfile(os.path.join('./db/', f))]
files.sort()
high_version = 0

for f in files:
    if f.split('.')[-1] == 'py':
        try:
            ver = int(f.split('_')[0])
        except:
            continue
        if ver > version:
            exec(open('./db/' + f).read())
            if ver > high_version:
                high_version = ver

print("Finished database migration, now version " + str(high_version))

set_key(dotenv_file, "DB_VERSION", str(high_version))
