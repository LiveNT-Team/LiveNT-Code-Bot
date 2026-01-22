-- 
-- depends: 20260118_01_pscu9

ALTER guilds
ADD COLUMN ai_chat_enabled BOOLEAN DEFAULT true,
ADD COLUMN ai_channel_id BIGINT UNSIGNED NULL;