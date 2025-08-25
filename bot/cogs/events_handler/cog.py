from disnake.ext.commands import Cog, Param, slash_command, CommandError, MissingPermissions
from disnake import AppCmdInter, Member, Message

from ...services.users.service import get_or_create_user
from ...core.database import session_factory
from ...core.logger import logger
from ...core.embeds import NotEnoughPermissionsEmbed


class EventsHandlerCog(Cog):
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
                    logger.info("Messages received, message counter increased.")

    @Cog.listener()
    async def on_slash_command_error(inter: AppCmdInter, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            logger.info("An attempt to execute an admin command without admin rights.")
            await inter.response.send_message(embed=NotEnoughPermissionsEmbed(), ephemeral=True)
        else:
            raise error

    @Cog.listener()
    async def on_ready() -> None:
        logger.info("Bot ready.")

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        # TODO: делать запрос к ии и приветствовать участника
        logger.info("Member joined.")
        ...


__all__ = ("EventsHandlerCog",)
