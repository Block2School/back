from pydantic import BaseModel

class ForumCommentModel(BaseModel):
    post_id: int
    # author_uuid: str
    text: str = None


# CREATE TABLE IF NOT EXISTS `comments` (
#     `id` INT NOT NULL AUTO_INCREMENT,
#     `post_id` INT,
#     `text` TEXT,
#     `author_uuid` VARCHAR(255) NOT NULL,
#     `time_created` TIMESTAMP NOT NULL DEFAULT NOW(),
#     PRIMARY KEY (`id`)
# );