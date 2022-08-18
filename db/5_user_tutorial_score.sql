CREATE TABLE `user_tutorial_score` (
    `uuid` VARCHAR(36) NOT NULL,
    `tutorial_id` INT(11) NOT NULL,
    `language` VARCHAR(255) NOT NULL,
    `characters` INT(11) NOT NULL,
    `lines` INT(11) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT `uuid_tutorial_id_language` UNIQUE (`uuid`, `tutorial_id`, `language`)
) DEFAULT CHARSET=utf8;