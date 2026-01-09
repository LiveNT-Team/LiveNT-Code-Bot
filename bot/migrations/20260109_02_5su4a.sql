-- 
-- depends: 20260109_01_5cRTG

CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    discord_gid BIGINT UNSIGNED,
    discord_uid BIGINT UNSIGNED,
    ai_per_name VARCHAR(32) NOT NULL,
    CONSTRAINT uc_gid_uid UNIQUE (discord_gid, discord_uid)
);