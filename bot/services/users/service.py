from services.mysqliup import MySqliUp
from core.models.user import User
from core.configuration import DEFAULT_PERSONALITY_NAME


async def get_user(
    db: MySqliUp,
    gid: int,
    uid: int,
) -> User | None:
    if row := await db.select_row(
        "users",
        [
            "id",
            "discord_gid",
            "discord_uid",
            "ai_per_name",
            "banned",
            "ban_expires_at",
            "ban_reason",
            "muted",
            "mut_expires_at",
            "mut_reason",
        ],
        where="discord_gid = %s AND discord_uid = %s",
        params=(
            gid,
            uid,
        ),
    ):
        return row
    return None


async def get_or_create_user(
    db: MySqliUp,
    gid: int,
    uid: int,
) -> User:
    if user := await get_user(db, gid, uid):
        return user
    await db.create_row(
        "users",
        {
            "discord_gid": gid,
            "discord_uid": uid,
            "ai_per_name": DEFAULT_PERSONALITY_NAME,
        },
    )
    if user := await get_user(db, gid, uid):
        return user
    else:
        raise ValueError("theaihopgg что за х***я")
