from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter

from services.guilds.service import get_or_create_by_discord_id
from services.mysqliup.service import MySqliUp
from core.base_embeds import InfoEmbed, SuccessEmbed
from core.embeds import NotEnoughPermissionsEmbed


class SettingsCog(Cog):
    # @slash_command()
    # async def template(self, inter: AppCmdInter) -> None:
    #     pass

    @slash_command()
    async def set(self, inter: AppCmdInter) -> None:
        pass

    @slash_command()
    async def get(self, inter: AppCmdInter) -> None:
        pass

    @get.sub_command("settings", "Выводит настройки бота для этого сервера")
    async def get_settings(self, inter: AppCmdInter) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        guild = await get_or_create_by_discord_id(db, gid=inter.guild_id)
        await db.commit()
        await db.close()
        settings_embed = InfoEmbed()
        settings_embed.add_field("Тестовая опция", str(guild.test_option))
        await inter.response.send_message(embed=settings_embed, ephemeral=True)

    @set.sub_command("test_option", "Изменение значения опции")
    async def set_test_option(
        self,
        inter: AppCmdInter,
        new_value: int = Param(
            1,
            description="Новое значение для параметра. Если пустое - значение по умолчанию",
        ),
    ) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await get_or_create_by_discord_id(db, gid=inter.guild_id)
        await db.update_row(
            "guilds",
            {"test_option": new_value},
            where="discord_gid = %s",
            where_params=(inter.guild_id,),
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("SettingsCog",)
