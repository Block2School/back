from pydantic import BaseModel

class ForumPostModel(BaseModel):
    title: str = None
    # author_uuid: int
    description: str = None
    category: str = None
    # image: str = None
    # points: int = None

# CREATE TABLE IF NOT EXISTS `forumPosts` (
#     `id` INT NOT NULL AUTO_INCREMENT,
#     `author_uuid` VARCHAR(255) NOT NULL,
#     `title` VARCHAR(255) NOT NULL,
#     `description` TEXT,
#     `points` INT NOT NULL,
#     `time_created` TIMESTAMP NOT NULL DEFAULT NOW(),
#     PRIMARY KEY (`id`)
# );