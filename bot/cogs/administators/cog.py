from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter, Role

from cogs.settings.decorators import has_developer_role
from core.base_embeds import SuccessEmbed
from services.guilds_settings.service import set_guild_settings_option
from services.guilds.service import get_or_create_guild
from services.mysqliup.service import MySqliUp


async def set_tole1

class AdministratorsCog(Cog):
    @slash_command()
    @has_developer_role
    async def set_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await get_or_create_guild(db, inter.guild_id)
        await set_guild_settings_option(
            db,
            "admin_role_id",
            role.id if role else None,
            gid=inter.guild_id,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())
    
    @slash_command()
    @has_developer_role
    async def set_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await get_or_create_guild(db, inter.guild_id)
        await set_guild_settings_option(
            db,
            "main_admin_role_id",
            role.id if role else None,
            gid=inter.guild_id,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())


"",
"",
"major_admin_role_id",
"minor_admin_role_id",
"main_moder_role_id",
"moder_role_id",
"major_moder_role_id",
"minor_moder_role_id",


__all__ = ("AdministratorsCog",)
