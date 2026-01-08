from core.models.guild import Guild
from services.mysqliup import MySqliUp


async def get_guild_by_discord_gid(db: MySqliUp, gid: int) -> Guild | None:
    if row := await db.select_row(
        "guilds",
        [
            "id",
            "discord_gid",
            "developer_role_id",
        ],
        where="discord_gid = %s",
        params=(gid,),
    ):
        return row
    return None


async def get_or_create_by_discord_id(db: MySqliUp, gid: int) -> Guild:
    if guild := await get_guild_by_discord_gid(db, gid):
        return guild
    await db.create_row("guilds", {"discord_gid": gid})
    if guild := await get_guild_by_discord_gid(db, gid):
        return guild
    else:
        raise ValueError("theaihopgg что за х***я")
