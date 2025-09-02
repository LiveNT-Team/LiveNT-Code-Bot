from disnake.ext.commands import Cog, Param, slash_command, String
from disnake import AppCmdInter, AllowedMentions


from .embeds import AIErrorEmbed
from ...services.aiu import send_ai_request
from ...services.users import get_or_create_user
from ...services.guilds_settings import get_or_create_guild_settings
from ...core.configuration import PERSONALITIES
from ...core.database import session_factory


class AICog(Cog):
    @slash_command()
    async def ask(
        self,
        inter: AppCmdInter,
        text: String[str, 3, 50],
        personality_name: str | None = Param(default=None, choices=list(PERSONALITIES.keys())),
    ) -> None:
        await inter.response.defer()
        async with session_factory() as session:
            guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
            if guild_settings.is_ai_enabled:
                async with inter.channel.typing():
                    if personality_name:
                        if ai_response := await send_ai_request(text=text, personality=PERSONALITIES[personality_name]):
                            await inter.edit_original_response(
                                content=ai_response,
                                allowed_mentions=AllowedMentions(
                                    everyone=False,
                                    users=False,
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
                        if ai_response := await send_ai_request(text=text, personality=PERSONALITIES[user.current_personality_name]):
                            await inter.edit_original_response(
                                content=ai_response,
                                allowed_mentions=AllowedMentions(
                                    everyone=False,
                                    users=False,
                                ),
                            )
                        else:
                            await inter.edit_original_response(embed=AIErrorEmbed())


__all__ = ("AICog",)
