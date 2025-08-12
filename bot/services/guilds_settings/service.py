from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.models import GuildSettings
from ...core.database import session_factory


async def get_guild_settings(session: AsyncSession, *, guild_id: int) -> GuildSettings | None:
    return (await session.execute(select(GuildSettings).where(GuildSettings.guild_id == guild_id))).scalar_one_or_none()


async def get_or_create_guild_settings(session: AsyncSession, *, guild_id: int) -> GuildSettings:
    if guild_settings := await get_guild_settings(session, guild_id=guild_id):
        return guild_settings
    else:
        guild_settings = GuildSettings(guild_id=guild_id)
        session.add(guild_settings)
        await session.commit()
        return guild_settings


__all__ = (
    "get_guild_settings",
    "get_or_create_guild_settings",
)
