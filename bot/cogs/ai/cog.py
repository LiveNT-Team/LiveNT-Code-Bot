from disnake.ext.commands import Cog, Param, slash_command, String, InteractionBot
from disnake import AllowedMentions, AppCmdInter, Attachment, Message
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.models import GuildSettings, User
from .embeds import AIErrorEmbed, AIIsDisabledEmbed
from ...services.aiu import send_ai_request
from ...services.users import get_or_create_user
from ...services.guilds_settings import get_or_create_guild_settings
from ...core.embeds import TheCommandDoesNotSupportDMEmbed
from ...core.configuration import PERSONALITIES, DEFAULT_PERSONALITY_NAME
from ...core.database import session_factory
from ...core.utils import split_into_chunks
from ...core.logger import logger
from ...core.base_embeds import SuccessEmbed


class AICog(Cog):
    @slash_command()
    async def ask(
        self,
        inter: AppCmdInter,
        text: String[str, 3, 200],
        personality_name: str | None = Param(
            default=None, choices=list(PERSONALITIES.keys())
        ),
    ) -> None:
        await inter.response.defer()
        if inter.guild:
            async with session_factory() as session:
                guild_settings = await get_or_create_guild_settings(
                    session, guild_id=inter.guild.id
                )
                await session.refresh(guild_settings)
                if guild_settings.is_ai_enabled:
                    if personality_name:
                        if ai_response := await send_ai_request(
                            text=text, personality=PERSONALITIES[personality_name]
                        ):
                            await inter.edit_original_response(embed=SuccessEmbed())
                            for chunk in split_into_chunks(ai_response):
                                await inter.channel.send(
                                    chunk,
                                    allowed_mentions=AllowedMentions(
                                        users=False,
                                        everyone=False,
                                    ),
                                )
                        else:
                            await inter.edit_original_response(embed=AIErrorEmbed())
                    else:
                        user = await get_or_create_user(
                            session,
                            discord_id=inter.author.id,
                            guild_id=inter.guild.id,
                        )
                        await session.refresh(user)
                        if ai_response := await send_ai_request(
                            text=text,
                            personality=PERSONALITIES[user.current_personality_name],
                        ):
                            await inter.edit_original_response(embed=SuccessEmbed())
                            for chunk in split_into_chunks(ai_response):
                                await inter.channel.send(
                                    chunk,
                                    allowed_mentions=AllowedMentions(
                                        users=False,
                                        everyone=False,
                                    ),
                                )
                        else:
                            await inter.edit_original_response(embed=AIErrorEmbed())
                else:
                    await inter.edit_original_response(embed=AIIsDisabledEmbed())
        else:
            await inter.response.send_message(
                embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True
            )

    @staticmethod
    async def handle_message(
        bot: InteractionBot,
        session: AsyncSession,
        message: Message,
        guild_settings: GuildSettings,
        author_user_model: User,
    ) -> None:
        def get_image_url_from_attachments(attachments: list[Attachment]) -> str | None:
            for attachment in attachments:
                logger.info(attachment.content_type)
                match attachment.content_type:
                    case (
                        "image/png"
                        | "image/jpg"
                        | "image/jpeg"
                        | "image/webp"
                        | "image/svg"
                    ):
                        return attachment.url
            return None

        if message.guild:
            if not message.author.bot:
                if (
                    bot.user in message.mentions
                    or message.channel.id == guild_settings.ai_channel_id
                ):
                    if guild_settings.is_ai_enabled:
                        if ai_response := await send_ai_request(
                            text=message.content,
                            personality=PERSONALITIES.get(
                                author_user_model.current_personality_name
                            )
                            or DEFAULT_PERSONALITY_NAME,
                            image_url=get_image_url_from_attachments(
                                message.attachments
                            ),
                        ):
                            for chunk in split_into_chunks(ai_response):
                                await message.channel.send(
                                    chunk,
                                    allowed_mentions=AllowedMentions(
                                        users=False,
                                        everyone=False,
                                    ),
                                )
                        else:
                            await message.reply(embed=AIErrorEmbed())


__all__ = ("AICog",)
