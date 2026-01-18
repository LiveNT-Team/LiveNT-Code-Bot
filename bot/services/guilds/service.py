from typing import Any
from core.models.guild import Guild
from services.mysqliup import MySqliUp


async def get_guild(db: MySqliUp, gid: int) -> Guild | None:
    if row := await db.select_row(
        "guilds",
        [
            "id",
            "discord_gid",
            "developer_role_id",
            "greetings_enabled",
            "greetings_channel_id",
        ],
        where="discord_gid = %s",
        params=(gid,),
    ):
        return row
    return None


async def get_or_create_guild(db: MySqliUp, gid: int) -> Guild:
    if guild := await get_guild(db, gid):
        return guild
    await db.create_row("guilds", {"discord_gid": gid})
    if guild := await get_guild(db, gid):
        return guild
    else:
        raise ValueError("theaihopgg что за х***я")


async def set_guild_setting(db: MySqliUp, gid: int, name: str, value: Any) -> None:
    await get_or_create_guild(db, gid)
    await db.update_row(
        "guilds",
        {name: value},
        where="discord_gid = %s",
        where_params=(gid,),
    )
