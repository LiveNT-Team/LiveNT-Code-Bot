-- 
-- depends: 20260122_01_1mPvH

CREATE TABLE bans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    discord_admin_id BIGINT UNSIGNED NOT NULL,
    discord_uid BIGINT UNSIGNED UNIQUE NOT NULL,
    discord_gid BIGINT UNSIGNED UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(64) DEFAULT "",
    CONSTRAINT uc_bans_gid_uid UNIQUE (discord_uid, discord_gid)
);

ALTER TABLE guilds
ADD COLUMN ban_role_id BIGINT NULL,
ADD COLUMN banning_enabled BIGINT NULL;