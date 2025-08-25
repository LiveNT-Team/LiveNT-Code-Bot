from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter, Member, Message

from ...core.database import session_factory
from ...services.users import get_or_create_user


class StatsCog(Cog):
    @slash_command()
    async def stats(
        self,
        inter: AppCmdInter,
        member: Member | None = None,
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
                    await inter.response.send_message(f"Статистика {member.mention}:\nСообщений отправлено: {user.messages_count}")
            else:
                await inter.response.send_message("ERROR2")
        else:
            await inter.response.send_message("ERROR1")

    @Cog.listener("on_message")
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


__all__ = ("StatsCog",)
