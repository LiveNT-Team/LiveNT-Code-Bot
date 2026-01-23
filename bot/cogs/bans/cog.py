from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter, Role, User
from enum import StrEnum

from core.base_embeds import SuccessEmbed
from core.embeds import NotEnoughPermissionsEmbed
from services.guilds.service import set_guild_setting
from services.mysqliup.service import MySqliUp
from cogs.settings.decorators import has_developer_role


class Duration(StrEnum):
    TEN_MINUTES = "10 минут"
    ONE_HOUR = "1 час"
    TWELVE_HOUR = "12 часов"
    ONE_DAY = "1 день"
    FIFTEEN_DAYS = "15 дней"
    ONE_MONTH = "1 месяц"


class BansCog(Cog):
    @slash_command()
    @has_developer_role
    async def enable_bans(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "bans_enabled", True)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def disable_bans(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "bans_enabled", False)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_bans_role(
        self,
        inter: AppCmdInter,
        role: Role | None = Param(
            description="Оставьте пустым для значния по умолчанию"
        ),
    ) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "ban_role_id",
            role.id if role else None,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    async def ban(
        self,
        inter: AppCmdInter,
        member: User,
        reason: str | None = None,
    ) -> None:
        pass

    @slash_command()
    async def unban(
        self,
        inter: AppCmdInter,
        member: User,
        reason: str | None = None,
    ) -> None:
        pass


__all__ = ("BansCog",)
