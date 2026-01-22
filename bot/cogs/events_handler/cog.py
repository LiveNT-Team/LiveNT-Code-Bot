from disnake.ext.commands import Cog, MissingPermissions, slash_command, Param
from disnake import AppCmdInter, Message, Member

from core.logger import logger
from core.embeds import NotEnoughPermissionsEmbed
from core.base_embeds import InfoEmbed
from services.mysqliup import MySqliUp
from services.users import increment_messages_count, get_or_create_user
from services.guilds import get_or_create_guild


class EventsHandlerCog(Cog):
    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot is ready")

    @Cog.listener()
    async def on_slash_command_error(self, inter: AppCmdInter, error: Exception):
        if isinstance(error, MissingPermissions):
            await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )
        else:
            raise error

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot or not message.guild:
            return
        db = MySqliUp()
        await db.connect()
        await db.begin()
        try:
            new_count = await increment_messages_count(
                db,
                message.guild.id,
                message.author.id,
            )
            guild = await get_or_create_guild(db, message.guild.id)
            await db.commit()
            if (
                guild["activist_enabled"]
                and guild["activist_role_id"]
                and guild["activist_messages_count"]
                and new_count >= guild["activist_messages_count"]
            ):
                role = message.guild.get_role(guild["activist_role_id"])
                if role and role not in message.author.roles:
                    await message.author.add_roles(role)
        except Exception:
            await db.rollback()
        finally:
            await db.close()

    @slash_command(description="Посмотреть количество отправленных сообщений")
    async def stats(
        self,
        inter: AppCmdInter,
        member: Member | None = Param(
            None, description="Участник для просмотра статистики"
        ),
    ) -> None:
        target = member or inter.author
        db = MySqliUp()
        await db.connect()
        await db.begin()
        user = await get_or_create_user(db, inter.guild_id, target.id)
        await db.commit()
        await db.close()
        embed = InfoEmbed()
        embed.title = "Статистика сообщений"
        embed.description = f"**{target.display_name}** отправил(а) **{user['messages_count']}** сообщений"
        await inter.response.send_message(embed=embed)


__all__ = ("EventsHandlerCog",)
