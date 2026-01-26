from mysql.connector.errors import Int
from datetime import timedelta, datetime
from core.models.ban import Ban
from services.mysqliup import MySqliUp


async def ban_user(
    db: MySqliUp,
    gid: int,
    uid: int,
    duration: timedelta,
    reason: str = "",
) -> None:
    await db.create_row(
        "bans",
        {
            "discord_uid": uid,
            "discord_gid": gid,
            "expires_at": datetime.now() + duration,
            "reason": reason,
        },
    )
    await db.commit()


async def unban_user(
    db: MySqliUp,
    gid: int,
    uid: int,
) -> None:
    await db.delete_row(
        "bans",
        where="discord_uid = %s AND discord_gid = %s",
        params=(
            uid,
            gid,
        ),
    )
    await db.commit()
