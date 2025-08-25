from disnake.ext.commands import Cog, Param, slash_command, has_permissions
from disnake import AppCmdInter, TextChannel

from ...core.database import session_factory
from ...services.guilds_settings import get_guild_settings, get_or_create_guild_settings


class SettingsCog(Cog):
    # region unusable commands
    @slash_command()
    async def set(self, inter: AppCmdInter) -> None:
        pass

    @slash_command()
    async def enable(self, inter: AppCmdInter) -> None:
        pass

    @slash_command()
    async def disable(self, inter: AppCmdInter) -> None:
        pass

    # endregion

    # region ai commands
    @enable.sub_command("ai")
    @has_permissions(administrator=True)
    async def enable_ai(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_ai_enabled = True
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    @disable.sub_command("ai")
    @has_permissions(administrator=True)
    async def disable_ai(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_ai_enabled = False
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    @set.sub_command("ai_channel")
    @has_permissions(administrator=True)
    async def set_ai_channel(
        self,
        inter: AppCmdInter,
        channel: TextChannel,
    ) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.ai_channel_id = channel.id
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    # endregion

    # region greetings commands
    @enable.sub_command("greetings")
    @has_permissions(administrator=True)
    async def enable_greetings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_greetings_enabled = True
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    @disable.sub_command("greetings")
    @has_permissions(administrator=True)
    async def disable_greetings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_greetings_enabled = False
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    @set.sub_command("greetings_channel")
    @has_permissions(administrator=True)
    async def set_greetings_channel(
        self,
        inter: AppCmdInter,
        channel: TextChannel,
    ) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.greetings_channel_id = channel.id
                await session.commit()
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    # endregion

    @slash_command(name="settings")
    @has_permissions(administrator=True)
    async def get_settings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                await inter.response.send_message(
                    f"ИИ канал: <#{guild_settings.ai_channel_id}>\nКанал приветствий: <#{guild_settings.greetings_channel_id}>\n{"Приветствия включены" if guild_settings.is_greetings_enabled else "Приветствия выключены"}\n{"ИИ включен" if guild_settings.is_ai_enabled else "ИИ выключен"}"
                )
        else:
            await inter.response.send_message("ERROR1")


__all__ = ("SettingsCog",)
