from disnake.ext.commands import Cog, Param, slash_command, has_permissions
from disnake import AppCmdInter, Role, TextChannel

from ...core.database import session_factory
from ...core.embeds import TheCommandDoesNotSupportDMEmbed
from ...services.guilds_settings import get_guild_settings, get_or_create_guild_settings
from .embeds import (
    AIChannelSetEmbed,
    AIDisabledEmbed,
    AIEnabledEmbed,
    ActivistExtraditingDisabledEmbed,
    ActivistExtraditingEnabledEmbed,
    ActivistMessagesCountCantBeLessThanZeroEmbed,
    ActivistMessagesCountSetEmbed,
    ActivistRoleSetEmbed,
    GreetingsChannelSetEmbed,
    GreetingsDisabledEmbed,
    GreetingsEnabledEmbed,
    SettingsEmbed,
)


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
    @enable.sub_command(
        name="ai",
        description="Включает ИИ функционал",
    )
    @has_permissions(administrator=True)
    async def enable_ai(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_ai_enabled = True
                await session.commit()
                await inter.response.send_message(embed=AIEnabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @disable.sub_command(
        name="ai",
        description="Выключает ИИ функционал",
    )
    @has_permissions(administrator=True)
    async def disable_ai(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_ai_enabled = False
                await session.commit()
                await inter.response.send_message(embed=AIDisabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @set.sub_command(
        name="ai_channel",
        description="Устанавливает канал для общения с ИИ моделью",
    )
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
                await inter.response.send_message(embed=AIChannelSetEmbed(channel=channel))
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    # endregion

    # region greetings commands
    @enable.sub_command(
        name="greetings",
        description="Включает приветствия для новых пользователей",
    )
    @has_permissions(administrator=True)
    async def enable_greetings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_greetings_enabled = True
                await session.commit()
                await inter.response.send_message(embed=GreetingsEnabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @disable.sub_command(
        name="greetings",
        description="Выключает приветствия для новых пользователей",
    )
    @has_permissions(administrator=True)
    async def disable_greetings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_greetings_enabled = False
                await session.commit()
                await inter.response.send_message(embed=GreetingsDisabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @set.sub_command(
        name="greetings_channel",
        description="Устанавливает канал для приветствия новых пользователей",
    )
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
                await inter.response.send_message(embed=GreetingsChannelSetEmbed(channel=channel))
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    # endregion

    # region activist commands
    @set.sub_command(name="activist_role")
    @has_permissions(administrator=True)
    async def set_activist_role(
        self,
        inter: AppCmdInter,
        role: Role,
    ) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild_id)
                guild_settings.activist_role_id = role.id
                await session.commit()
                await inter.response.send_message(embed=ActivistRoleSetEmbed())

    @set.sub_command(name="activist_messages_count")
    @has_permissions(administrator=True)
    async def set_activist_messages_count(
        self,
        inter: AppCmdInter,
        count: int,
    ) -> None:
        if inter.guild:
            if count > 0:
                async with session_factory() as session:
                    guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild_id)
                    guild_settings.activist_role_messages_count = count
                    await session.commit()
                    await inter.response.send_message(embed=ActivistMessagesCountSetEmbed())
            else:
                await inter.response.send_message(embed=ActivistMessagesCountCantBeLessThanZeroEmbed(), ephemeral=True)

    @enable.sub_command(
        name="extraditing_activist",
    )
    @has_permissions(administrator=True)
    async def enable_extraditing_activist(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_activist_role_extraditing = True
                await session.commit()
                await inter.response.send_message(embed=ActivistExtraditingEnabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @disable.sub_command(
        name="extraditing_activist",
    )
    @has_permissions(administrator=True)
    async def disable_extraditing_activist(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                guild_settings.is_activist_role_extraditing = False
                await session.commit()
                await inter.response.send_message(embed=ActivistExtraditingDisabledEmbed())
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    # endregion

    @slash_command(
        name="settings",
        description="Выводит настройки сервера",
    )
    @has_permissions(administrator=True)
    async def get_settings(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
                await inter.response.send_message(
                    embed=SettingsEmbed(
                        greetings_channel_id=guild_settings.greetings_channel_id,
                        ai_channel_id=guild_settings.ai_channel_id,
                        is_greetings_enabled=guild_settings.is_greetings_enabled,
                        is_ai_enabled=guild_settings.is_ai_enabled,
                        is_activist_role_extraditing=guild_settings.is_activist_role_extraditing,
                        activist_role_id=guild_settings.activist_role_id,
                        activist_role_messages_count=guild_settings.activist_role_messages_count,
                    ),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)


__all__ = ("SettingsCog",)
