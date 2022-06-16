CREATE TABLE IF NOT EXISTS `account` (
    `uuid` VARCHAR(36) NOT NULL,
    `wallet_address` VARCHAR(255) NOT NULL,
    `is_banned` BOOLEAN NOT NULL DEFAULT false,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`uuid`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `account_details` (
    `uuid` VARCHAR(36) NOT NULL,
    `wallet_address` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`uuid`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `account_moderation` (
    `uuid` VARCHAR(36) NOT NULL,
    `role` INT(11) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (`uuid`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `account_punishment` (
    `uuid` VARCHAR(36) NOT NULL,
    `reason` VARCHAR(255) NOT NULL,
    `banned_by` VARCHAR(36) NOT NULL,
    `expires` TIMESTAMP,
    `is_revoked` BOOLEAN NOT NULL DEFAULT false,
    `revoked_by` VARCHAR(36),
    `revoke_reason` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
    `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
    INDEX (`uuid`)
) DEFAULT CHARSET=utf8;