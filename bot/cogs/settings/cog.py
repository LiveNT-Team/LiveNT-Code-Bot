from disnake.ext.commands import Cog, Param, slash_command, has_permissions
from disnake import AppCmdInter, Role, TextChannel

from services.guilds.service import get_or_create_guild, set_guild_setting
from services.mysqliup.service import MySqliUp
from core.base_embeds import InfoEmbed, SuccessEmbed
from core.embeds import NotEnoughPermissionsEmbed
from .decorators import has_developer_role


class SettingsCog(Cog):
    @slash_command(description="Выводит настройки бота для этого сервера")
    @has_developer_role
    async def get_settings(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        guild = await get_or_create_guild(db, inter.guild_id)
        await db.commit()
        await db.close()
        settings_embed = InfoEmbed()
        settings_embed.add_field(
            "Роль разработчика",
            (
                f"<@&{guild['developer_role_id']}>"
                if guild["developer_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль главного администратора",
            (
                f"<@&{guild["main_admin_role_id"]}>"
                if guild["main_admin_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль старшего администратора",
            (
                f"<@&{guild["major_admin_role_id"]}>"
                if guild["major_admin_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль администратора",
            (
                f"<@&{guild["admin_role_id"]}>"
                if guild["admin_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль младшего администратора",
            (
                f"<@&{guild["minor_admin_role_id"]}>"
                if guild["minor_admin_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль главного модератора",
            (
                f"<@&{guild["main_moder_role_id"]}>"
                if guild["main_moder_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль старшего модератора",
            (
                f"<@&{guild["major_moder_role_id"]}>"
                if guild["major_moder_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль модератора",
            (
                f"<@&{guild["moder_role_id"]}>"
                if guild["moder_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Роль младшего модератора",
            (
                f"<@&{guild["minor_moder_role_id"]}>"
                if guild["minor_moder_role_id"]
                else "Не задана"
            ),
            inline=False,
        )
        settings_embed.add_field(
            "Приветствия",
            "Включены" if guild["greetings_enabled"] else "Выключены",
        )
        settings_embed.add_field(
            "Канал приветствий",
            (
                f"<#{guild['greetings_channel_id']}>"
                if guild["greetings_channel_id"]
                else "Не задан"
            ),
        )
        await inter.response.send_message(embed=settings_embed, ephemeral=True)

    @slash_command(name="set_developer_role", description="Изменение роли разработчика")
    @has_permissions(administrator=True)
    async def set_developer_role(
        self,
        inter: AppCmdInter,
        new_role: Role | None = Param(
            None,
            description="Новое значение для параметра. Если пустое - значение по умолчанию",
        ),
    ) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "developer_role_id",
            new_role.id if new_role else None,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("SettingsCog",)
