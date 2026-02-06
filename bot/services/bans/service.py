from datetime import timedelta, datetime
from pymysql.err import IntegrityError

from core.models.ban import Ban
from services.mysqliup import MySqliUp


async def ban_user(
    db: MySqliUp,
    gid: int,
    uid: int,
    discord_admin_id: int,
    duration: timedelta,
    reason: str = "",
) -> None:
    try:
        await db.create_row(
            "bans",
            {
                "discord_admin_id": discord_admin_id,
                "discord_uid": uid,
                "discord_gid": gid,
                "expires_at": datetime.now() + duration,
                "reason": reason,
            },
        )
    except IntegrityError:
        await db.update_row(
            "bans",
            {
                "discord_admin_id": discord_admin_id,
                "expires_at": datetime.now() + duration,
                "reason": reason,
            },
            where="discord_uid = %s AND discord_gid = %s",
            where_params=(uid, gid),
        )
    finally:
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


async def get_bans_per_day_count(db: MySqliUp, discord_admin_id: int) -> int:
    now = datetime.now()
    day_beginning = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        second=0,
        minute=0,
        hour=0,
    )
    day_ending = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        second=59,
        minute=59,
        hour=23,
    )
    return await db.select_count_all_row(
        "bans",
        where="discord_admin_id = %s AND created_at >= %s AND created_at <= %s",
        params=(
            discord_admin_id,
            day_beginning,
            day_ending,
        ),
    )


async def get_expired_bans(db: MySqliUp, gid: int) -> list[Ban]:
    return await db.select_rows(
        "bans",
        (
            "id",
            "discord_admin_id",
            "discord_uid",
            "discord_gid",
            "expires_at",
            "created_at",
            "reason",
        ),
        where="expires_at < %s AND discord_gid = %s",
        params=(
            datetime.now(),
            gid,
        ),
    )


async def get_ban_info(db: MySqliUp, uid: int, gid: int) -> Ban | None:
    return await db.select_row(
        "bans",
        (
            "id",
            "discord_admin_id",
            "discord_uid",
            "discord_gid",
            "expires_at",
            "created_at",
            "reason",
        ),
        where="discord_uid = %s AND discord_gid = %s",
        params=(uid, gid),
    )
