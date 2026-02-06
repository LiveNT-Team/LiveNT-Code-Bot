from disnake.ext.commands import Cog, slash_command
from disnake import AppCmdInter, Role

from cogs.settings.decorators import has_developer_role
from core.base_embeds import SuccessEmbed
from services.guilds.service import get_or_create_guild, set_guild_setting
from services.mysqliup.service import MySqliUp


async def set_special_role(role: Role | None, field_name: str, gid: int) -> None:
    db = MySqliUp()
    await db.connect()
    await db.begin()
    await get_or_create_guild(db, gid)
    await set_guild_setting(
        db,
        name=field_name,
        value=role.id if role else None,
        gid=gid,
    )
    await db.commit()
    await db.close()


class AdministratorsCog(Cog):
    @slash_command()
    @has_developer_role
    async def set_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "admin_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_main_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "main_admin_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_major_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "major_admin_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_minor_admin_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "minor_admin_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_moder_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "moder_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_main_moder_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "main_moder_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_major_moder_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "major_moder_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_minor_moder_role(
        self,
        inter: AppCmdInter,
        role: Role | None = None,
    ) -> None:
        await set_special_role(role, "minor_moder_role_id", inter.guild_id)
        await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("AdministratorsCog",)
