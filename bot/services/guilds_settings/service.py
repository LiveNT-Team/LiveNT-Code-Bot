from typing import Any
from services.mysqliup import MySqliUp
from services.guilds.service import get_or_create_guild


async def set_guild_settings_option(
	db: MySqliUp,
	name: str,
	value: Any,
	gid: int,
) -> None:
	await get_or_create_guild(db, gid=gid)
	await db.update_row(
		"guilds",
		{name: value},
		where="discord_gid = %s",
		where_params=(gid,),
	)


async def enable_greetings(db: MySqliUp, gid: int) -> None:
	await set_guild_settings_option(db, "greetings_enabled", True, gid)


async def disable_greetings(db: MySqliUp, gid: int) -> None:
	await set_guild_settings_option(db, "greetings_enabled", False, gid)


async def set_greetings_channel(db: MySqliUp, gid: int, channel_id: int | None) -> None:
	await set_guild_settings_option(db, "greetings_channel_id", channel_id, gid)
