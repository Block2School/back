CREATE TABLE IF NOT EXISTS `tutorials` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `markdown_url` VARCHAR(255) NOT NULL,
    `category` VARCHAR(255) NOT NULL,
    `answer` TEXT NOT NULL,
    `start_code` TEXT NOT NULL,
    `should_be_check` BOOLEAN NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;