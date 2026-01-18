from disnake.ext.commands import Cog, InteractionBot
from disnake import Member

from services.mysqliup.service import MySqliUp
from services.guilds.service import get_guild
from services.prompts.service import get_greetings_text


class EventsHandlerCog(Cog):
    def __init__(self, bot: InteractionBot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        db = MySqliUp()
        await db.connect()
        guild = await get_guild(db, member.guild.id)
        await db.close()
        if not guild:
            return
        if not guild["greetings_enabled"]:
            return
        if not guild["greetings_channel_id"]:
            return
        channel = self.bot.get_channel(guild["greetings_channel_id"])
        if not channel:
            return
        text = await get_greetings_text(member)
        if text:
            await channel.send(text)


__all__ = ("EventsHandlerCog",)
