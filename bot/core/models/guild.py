from typing import TypedDict


class Guild(TypedDict):
	id: int
	discord_gid: int
	developer_role_id: int
	greetings_enabled: bool
	greetings_channel_id: int
