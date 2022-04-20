import os
from dotenv import load_dotenv
import postgresql

load_dotenv()

db = postgresql.open('pq://%s:%s@%s:%d/%s' %
                    (os.getenv('PG_USER'), os.getenv('PG_PASSWORD'),
                    os.getenv('PG_HOST'), int(os.getenv('PG_PORT')),
                    os.getenv('PG_DATABASE')))