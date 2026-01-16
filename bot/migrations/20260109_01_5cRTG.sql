--
-- depends:

CREATE TABLE guilds (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    discord_gid BIGINT UNSIGNED UNIQUE,
    developer_role_id BIGINT UNSIGNED NULL,
    greetings_enabled BOOLEAN DEFAULT FALSE,
    greetings_channel_id BIGINT UNSIGNED NULL
);