from disnake import AppCmdInter
from typing import Callable, Awaitable
from functools import wraps
from services.mysqliup.service import MySqliUp
from core.embeds import NotEnoughPermissionsEmbed
from services.guilds.service import get_or_create_guild


def has_developer_role(func: Callable[..., Awaitable]):
    """Проверяет автора взаимодействия на наличие роли разработчика или прав администратора"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        inter: AppCmdInter = kwargs["inter"]
        db = MySqliUp()
        await db.connect()
        await db.begin()

        if inter.author.guild_permissions.administrator:
            return await func(*args, **kwargs)

        guild = await get_or_create_guild(db, gid=inter.guild_id)
        await db.commit()

        if not guild["developer_role_id"]:
            return await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )

        developer_role = inter.guild.get_role(guild["developer_role_id"])
        if not developer_role:
            return await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )

        if not developer_role in inter.author.roles:
            return await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )

        await db.close()
        return await func(*args, **kwargs)

    return wrapper
