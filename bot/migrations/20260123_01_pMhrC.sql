-- 
-- depends: 20260122_01_1mPvH

CREATE TABLE bans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    discord_uid BIGINT UNSIGNED UNIQUE NOT NULL,
    discord_gid BIGINT UNSIGNED UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    reason VARCHAR(64) DEFAULT "",
    FOREIGN KEY discord_uid REFERENCES users(discord_uid),
    FOREIGN KEY discord_gid REFERENCES users(discord_gid),
    CONSTRAINT uc_bans_gid_uid UNIQUE (discord_uid, discord_gid)
);

ALTER TABLE guilds
ADD COLUMN ban_role_id BIGINT NULL,
ADD COLUMN banning_enabled BIGINT NULL;