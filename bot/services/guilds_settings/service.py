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
        {"developer_role_id": value},
        where="discord_gid = %s",
        where_params=(gid,),
    )
