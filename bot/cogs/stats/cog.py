from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter, Member, Message

from bot.cogs.stats.embeds import MemberStatsEmbed

from ...core.database import session_factory
from ...core.embeds import YouCannotMentionBotInsteadMemberEmbed, TheCommandDoesNotSupportDMEmbed
from ...services.users import get_or_create_user


class StatsCog(Cog):
    @slash_command(name="stats", description="Выводит статистику участника")
    async def stats(
        self,
        inter: AppCmdInter,
        member: Member | None = Param(default=None, description="Если не указан - будет выведена ваша статистика"),
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


__all__ = ("StatsCog",)
