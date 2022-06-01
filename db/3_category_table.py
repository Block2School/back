from database import get_database
import postgresql

db = get_database()
prepare = db.prepare('CREATE TABLE category(\
    name character varying NOT NULL,\
    description character varying NOT NULL,\
    image_url character varying NOT NULL,\
    created_at timestamp NOT NULL DEFAULT NOW(),\
    updated_at timestamp NOT NULL DEFAULT NOW(),\
    PRIMARY KEY(name));')
prepare()
prepare = db.prepare('CREATE TRIGGER set_timestamp\
    BEFORE UPDATE\
    ON category\
    FOR EACH ROW\
    EXECUTE PROCEDURE trigger_set_timestamp();')
prepare()
