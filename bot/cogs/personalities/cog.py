from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter

from services.mysqliup.service import MySqliUp
from services.users.service import get_or_create_user
from core.base_embeds import InfoEmbed, ErrorEmbed, SuccessEmbed
from core.configuration import PERSONALITIES


class PersonalitiesCog(Cog):
    # @slash_command()
    # async def template(self, inter: AppCmdInter) -> None:
    #     pass

    @slash_command(description="Выводит текущею личность ИИ ассистента")
    async def get_ai_personality(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        user = await get_or_create_user(db, gid=inter.guild_id, uid=inter.author.id)
        await db.commit()
        await db.close()
        personality = PERSONALITIES[user["ai_per_name"]]
        await inter.response.send_message(
            embed=InfoEmbed(description="Текущая личность ИИ ассистента`").add_field(
                user["ai_per_name"].upper(),
                f"**Название:** {personality['name']}\n\
                **Описание:** {personality['description']}\n\
                **Температура:** {personality['temperature']}\n\
                **Максимальное количество токенов:** {personality['max_tokens']}",
            ),
            ephemeral=False,
        )

    @slash_command(description="Устанавливает новую личность для ИИ ассистента")
    async def set_ai_personality(
        self,
        inter: AppCmdInter,
        new_personality_name: str = Param(choices=list(PERSONALITIES.keys())),
    ) -> None:
        if not new_personality_name in PERSONALITIES:
            return await inter.response.send_message(
                embed=ErrorEmbed(
                    description="Неизвестное название личности ИИ ассистента"
                )
            )
        db = MySqliUp()
        await db.connect()
        await db.begin()
        user = await get_or_create_user(db, gid=inter.guild_id, uid=inter.author.id)
        await db.update_row(
            "users",
            updates={
                "ai_per_name": new_personality_name,
            },
            where="id = %s",
            where_params=(user["id"],),
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command(description="Выводит список доступных личностей для ИИ бота")
    async def get_personalities(self, inter: AppCmdInter) -> None:
        embed = InfoEmbed(description="Информация о доступных личностях чат ассистента")
        for name, personality in PERSONALITIES.items():
            embed.add_field(
                name.upper(),
                f"**Название:** {personality['name']}\n\
                **Описание:** {personality['description']}\n\
                **Температура:** {personality['temperature']}\n\
                **Максимальное количество токенов:** {personality['max_tokens']}",
                inline=False,
            )
        await inter.response.send_message(embed=embed, ephemeral=False)


__all__ = ("PersonalitiesCog",)
