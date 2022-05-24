from database import get_database
import postgresql

db = get_database()

prepare = db.prepare('CREATE TABLE tutorials(\
    id int NOT NULL,\
    title character varying NOT NULL,\
    markdown_url character varying NOT NULL,\
    category character varying NOT NULL,\
    answer text NOT NULL,\
    start_code text NOT NULL,\
    should_be_check boolean NOT NULL,\
    created_at timestamp NOT NULL,\
    updated_at timestamp NOT NULL,\
    PRIMARY KEY(id));')
prepare()
prepare = db.prepare('CREATE TRIGGER set_timestamp\
    BEFORE UPDATE\
    ON tutorials\
    FOR EACH ROW\
    EXECUTE PROCEDURE trigger_set_timestamp();')
prepare()