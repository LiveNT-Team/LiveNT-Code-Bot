-- 
-- depends: 20260110_01_Jm3ud

ALTER TABLE guilds
ADD COLUMN greetings_enabled BOOLEAN DEFAULT FALSE,
ADD COLUMN greetings_channel_id BIGINT UNSIGNED NULL;