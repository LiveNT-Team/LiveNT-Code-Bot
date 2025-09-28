from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.models import User


async def get_user(
    session: AsyncSession,
    *,
    guild_id: int,
    discord_id: int,
) -> User | None:
    return (
        await session.execute(
            select(User).where(
                User.guild_id == guild_id,
                User.discord_id == discord_id,
            )
        )
    ).scalar_one_or_none()


async def get_or_create_user(
    session: AsyncSession,
    *,
    guild_id: int,
    discord_id: int,
) -> User:
    if user := await get_user(
        session,
        guild_id=guild_id,
        discord_id=discord_id,
    ):
        return user
    else:
        user = User(guild_id=guild_id, discord_id=discord_id)
        session.add(user)
        await session.commit()
        return user


__all__ = (
    "get_user",
    "get_or_create_user",
)
