CREATE TABLE IF NOT EXISTS `challenges` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `inputs` JSON NOT NULL,
    `answers` JSON NOT NULL,
    `markdown_url` VARCHAR(255) NOT NULL,
    `start_code` TEXT,
    `points` INT NOT NULL,
    `title` VARCHAR(45) NOT NULL,
    `language` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `challenges_completed` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_uuid` VARCHAR(36) NOT NULL,
    `challenge_id` INT NOT NULL,
    `completed_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `challenges_leaderboard` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_uuid` VARCHAR(36) NOT NULL,
    `points` INT NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `user_uuid_idx` (`user_uuid` ASC) VISIBLE,
    CONSTRAINT `user_uuid` FOREIGN KEY (`user_uuid`) REFERENCES `account` (`uuid`)
) DEFAULT CHARSET=utf8;