DROP TABLE `user_tutorial_score`;
DROP TABLE `account_tutorial_completion`;

CREATE TABLE IF NOT EXISTS `user_tutorial_score` (
    `uuid` VARCHAR(36) NOT NULL,
    `tutorial_id` INT(11) NOT NULL,
    `total_completions` INT(11) NOT NULL DEFAULT 1,
    `language` VARCHAR(255) NOT NULL,
    `characters` INT(11) NOT NULL,
    `lines` INT(11) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),

    CONSTRAINT `uuid_tutorial_id` UNIQUE (`uuid`, `tutorial_id`)
) DEFAULT CHARSET=utf8;