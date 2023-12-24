ALTER TABLE `tutorials`
ADD (`image` VARCHAR(255) DEFAULT NULL);

ALTER TABLE `tutorials`
ADD (`short_description` VARCHAR(255) DEFAULT NULL);

ALTER TABLE `tutorials`
ADD (`estimated_time` VARCHAR(255) DEFAULT NULL);

ALTER TABLE `tutorials`
ADD (`default_language` VARCHAR(255) DEFAULT NULL);

CREATE TABLE IF NOT EXISTS `completed_tutorials`(
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` VARCHAR(36) NOT NULL,
    `tutorial_id` INT(11) NOT NULL,
    `completed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `account`(`uuid`),
    FOREIGN KEY (`tutorial_id`) REFERENCES `tutorials`(`id`),
    UNIQUE KEY `user_tutorial` (`user_id`, `tutorial_id`)
) DEFAULT CHARSET=utf8;