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
            "messages_count",
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
            "messages_count": 0,
        },
    )
    if user := await get_user(db, gid, uid):
        return user
    else:
        raise ValueError("theaihopgg что за х***я")


async def increment_messages_count(
    db: MySqliUp,
    gid: int,
    uid: int,
) -> int:
    user = await get_or_create_user(db, gid, uid)
    new_count = user["messages_count"] + 1
    await db.update_row(
        "users",
        {"messages_count": new_count},
        where="discord_gid = %s AND discord_uid = %s",
        where_params=(gid, uid),
    )
    return new_count
