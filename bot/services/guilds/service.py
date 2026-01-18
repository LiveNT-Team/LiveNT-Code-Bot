from core.models.guild import Guild
from services.mysqliup import MySqliUp


async def get_guild(db: MySqliUp, gid: int) -> Guild | None:
    if row := await db.select_row(
        "guilds",
        [
            "id",
            "discord_gid",
            "developer_role_id",
            "main_admin_role_id",
            "admin_role_id",
            "major_admin_role_id",
            "minor_admin_role_id",
            "main_moder_role_id",
            "moder_role_id",
            "major_moder_role_id",
            "minor_moder_role_id",
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
