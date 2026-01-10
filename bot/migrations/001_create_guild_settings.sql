CREATE TABLE IF NOT EXISTS `guild_settings` (
    `guild_id` BIGINT UNSIGNED PRIMARY KEY,
    `is_greetings_enabled` TINYINT(1) DEFAULT 0,
    `greetings_channel_id` BIGINT UNSIGNED DEFAULT NULL,
    `is_ai_enabled` TINYINT(1) DEFAULT 0,
    `ai_channel_id` BIGINT UNSIGNED DEFAULT NULL,
    `developer_role_id` BIGINT UNSIGNED DEFAULT NULL,
    `activist_role_id` BIGINT UNSIGNED DEFAULT NULL,
    `activist_role_messages_count` INT UNSIGNED DEFAULT 0,
    `is_activist_role_extraditing` TINYINT(1) DEFAULT 0
);
