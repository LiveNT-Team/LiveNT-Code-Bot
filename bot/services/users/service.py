from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.models import User
from ...core.database import session_factory


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
    if guild_settings := await get_user(session, guild_id=guild_id):
        return guild_settings
    else:
        guild_settings = User(guild_id=guild_id, discord_id=discord_id)
        session.add(guild_settings)
        await session.commit()
        return guild_settings


__all__ = (
    "get_user",
    "get_or_create_user",
)
