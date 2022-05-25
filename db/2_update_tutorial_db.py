from database import get_database
import postgresql

db = get_database()

prepare = db.prepare('ALTER TABLE tutorials\
    ADD enabled boolean NOT NULL DEFAULT false;')
prepare()