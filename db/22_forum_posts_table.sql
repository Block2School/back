CREATE TABLE IF NOT EXISTS `forumPosts` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `author_uuid` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `points` INT NOT NULL,
    `time_created` TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `post_id` INT,
    `text` TEXT,
    `author_uuid` VARCHAR(255) NOT NULL,
    `time_created` TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`)
);