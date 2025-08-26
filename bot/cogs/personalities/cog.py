from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter

from ...core.database import session_factory
from ...core.configuration import PERSONALITIES
from ...core.embeds import TheCommandDoesNotSupportDMEmbed
from ...services.users import get_or_create_user
from .embeds import PersonalitiesListEmbed, PersonalitySetEmbed


class PersonalitiesCog(Cog):
    # region unusable commands
    @slash_command()
    async def change(self, inter: AppCmdInter) -> None:
        pass

    @slash_command()
    async def get(self, inter: AppCmdInter) -> None:
        pass

    # endregion
    @change.sub_command(
        name="personality",
        description="Изменяет личность ИИ модели. ИИ модель будет отвечать вам с учётом личности",
    )
    async def change_personality(
        self,
        inter: AppCmdInter,
        personality_name: str = Param(
            description="Название личности",
            choices=list(PERSONALITIES.keys()),
        ),
    ) -> None:
        if inter.guild:
            async with session_factory() as session:
                user = await get_or_create_user(
                    session,
                    discord_id=inter.author.id,
                    guild_id=inter.guild.id,
                )
                user.current_personality_name = personality_name
                await session.commit()
                await inter.response.send_message(embed=PersonalitySetEmbed(personality_name=personality_name))
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)

    @get.sub_command(
        name="personalities",
        description="Выводит список доступных личностей с их описаниями",
    )
    async def get_personalities(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                user = await get_or_create_user(
                    session,
                    guild_id=inter.guild.id,
                    discord_id=inter.author.id,
                )
                await inter.response.send_message(
                    embed=PersonalitiesListEmbed(current_personality_name=user.current_personality_name),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(embed=TheCommandDoesNotSupportDMEmbed(), ephemeral=True)


__all__ = ("PersonalitiesCog",)
