CREATE TABLE IF NOT EXISTS `friends` (
    `uuid` VARCHAR(36) NOT NULL,
    `friend_uuid` VARCHAR(36) NOT NULL,
    `status` VARCHAR(10) NOT NULL DEFAULT 'pending',
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT `uuid_friend_uuid` UNIQUE (`uuid`, `friend_uuid`),
    INDEX (`uuid`)
) DEFAULT CHARSET=utf8;