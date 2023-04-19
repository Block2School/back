CREATE TABLE IF NOT EXISTS `account_tutorial_completion` (
    `uuid` VARCHAR(36) NOT NULL,
    `tutorial_id` INT(11) NOT NULL,
    `total_completions` INT(11) NOT NULL DEFAULT 1,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT `uuid_tutorial_id` UNIQUE (`uuid`, `tutorial_id`)
) DEFAULT CHARSET=utf8;