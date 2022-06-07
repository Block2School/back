from database import get_database
import postgresql

db = get_database()

prepare = db.prepare('CREATE TABLE account_tutorial_completion(\
    uuid character varying NOT NULL,\
    tutorial_id integer NOT NULL,\
    total_completions integer NOT NULL DEFAULT 1,\
    created_at timestamp NOT NULL DEFAULT NOW(),\
    updated_at timestamp NOT NULL DEFAULT NOW(),\
    UNIQUE(uuid, tutorial_id));')
prepare()
prepare = db.prepare('CREATE TRIGGER set_timestamp\
    BEFORE UPDATE\
    ON account_tutorial_completion\
    FOR EACH ROW\
    EXECUTE PROCEDURE trigger_set_timestamp();')
prepare()
prepare = db.prepare('CREATE INDEX uuid_account_tutorial_completion_index\
    ON account_tutorial_completion (uuid);')
prepare()