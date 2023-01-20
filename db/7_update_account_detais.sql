ALTER TABLE `account_details`
ADD (`description` VARCHAR(255) DEFAULT NULL,
    `twitter` VARCHAR(100) DEFAULT NULL,
    `youtube` VARCHAR(100) DEFAULT NULL,
    `birthdate` DATE DEFAULT NULL);

CREATE TABLE `user_access` (
    `uuid` VARCHAR(36) NOT NULL,
    `data` VARCHAR(30) NOT NULL,
    `access` VARCHAR(30) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    CONSTRAINT `uuid_date` UNIQUE (`uuid`, `data`),
    INDEX (`uuid`)
) DEFAULT CHARSET=utf8;