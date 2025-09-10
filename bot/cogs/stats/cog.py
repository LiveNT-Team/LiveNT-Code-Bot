from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter, Forbidden, Member, Message

from ...core.logger import logger
from ...core.database import session_factory
from ...core.embeds import YouCannotMentionBotInsteadMemberEmbed, TheCommandDoesNotSupportDMEmbed
from ...services.users import get_or_create_user
from ...services.guilds_settings.service import get_or_create_guild_settings
from .embeds import MemberStatsEmbed, ActivistRoleAwardedEmbed


class StatsCog(Cog):
    @slash_command(
        name="stats",
        description="Выводит статистику участника",
    )
    async def stats(
        self,
        inter: AppCmdInter,
        member: Member | None = Param(
            default=None,
            description="Если не указан - будет выведена ваша статистика",
        ),
    ) -> None:
        if inter.guild:
            member = member or inter.author
            if not member.bot:
                async with session_factory() as session:
                    user = await get_or_create_user(
                        session,
                        guild_id=inter.guild.id,
                        discord_id=member.id,
                    )
                    await session.refresh(user)
                    await inter.response.send_message(
                        embed=MemberStatsEmbed(
                            member=member,
                            messages_count=user.messages_count,
                        )
                    )
            else:
                await inter.response.send_message(embed=YouCannotMentionBotInsteadMemberEmbed(), ephemeral=True)
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild:
            if not message.author.bot:
                async with session_factory() as session:
                    user = await get_or_create_user(
                        session,
                        guild_id=message.guild.id,
                        discord_id=message.author.id,
                    )
                    await session.refresh(user)
                    user.messages_count += 1
                    await session.commit()
                    guild_settings = await get_or_create_guild_settings(session, guild_id=message.guild.id)
                    await session.refresh(guild_settings)
                    if guild_settings.is_activist_role_extraditing and guild_settings.activist_role_messages_count:
                        await session.refresh(user)
                        await session.refresh(guild_settings)
                        if user.messages_count >= guild_settings.activist_role_messages_count:
                            if activist_role := message.guild.get_role(guild_settings.activist_role_id):
                                try:
                                    await message.author.add_roles(activist_role)
                                    await message.channel.send(embed=ActivistRoleAwardedEmbed(member=message.author))
                                except Forbidden:
                                    logger.error("Bot is missing access to award an activist role")


__all__ = ("StatsCog",)
