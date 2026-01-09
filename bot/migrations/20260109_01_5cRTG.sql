-- 
-- depends: 

CREATE TABLE guilds (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    discord_gid BIGINT UNSIGNED UNIQUE,
    developer_role_id BIGINT UNSIGNED NULL
);