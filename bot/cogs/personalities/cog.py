from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter

from ...core.database import session_factory
from ...core.configuration import PersonalitiesEnum, PERSONALITIES
from ...services.users import get_or_create_user


class PersonalitiesCog(Cog):
    # region unusable commands
    @slash_command()
    async def change(self, inter: AppCmdInter) -> None:
        pass

    @slash_command()
    async def get(self, inter: AppCmdInter) -> None:
        pass

    # endregion
    @change.sub_command(name="personality")
    async def set_personality(
        self,
        inter: AppCmdInter,
        personality_name: PersonalitiesEnum,
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
                await inter.response.send_message("SUCCESS")
        else:
            await inter.response.send_message("ERROR1")

    @get.sub_command(name="personalities")
    async def get_personalities(self, inter: AppCmdInter) -> None:
        if inter.guild:
            await inter.response.send_message("\n".join([f"{key} - {value}" for key, value in PERSONALITIES.items()]))
        else:
            await inter.response.send_message("ERROR1")


__all__ = ("PersonalitiesCog",)
