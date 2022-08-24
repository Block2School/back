CREATE TABLE `articles` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `markdown_url` VARCHAR(255) NOT NULL,
    `short_description` VARCHAR(255) NOT NULL,
    `author` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;