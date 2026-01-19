from disnake.ext.commands import (
    Cog,
    Param,
    slash_command,
    has_permissions,
    InteractionBot,
)
from disnake import AppCmdInter, Member, TextChannel

from services.prompts.service import get_greetings_text
from core.base_embeds import SuccessEmbed
from core.embeds import NotEnoughPermissionsEmbed
from services.guilds.service import get_guild, set_guild_setting
from services.mysqliup.service import MySqliUp


class GreetingsCog(Cog):
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
        channel = member.guild.get_channel(guild["greetings_channel_id"])
        if not channel:
            return
        text = await get_greetings_text(member)
        if text:
            await channel.send(text)

    @slash_command(description="Включить приветствия")
    @has_permissions(administrator=True)
    async def greetings(self, inter: AppCmdInter) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "greetings_enabled",
            True,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command(
        name="greetings",
        description="Выключить приветствия",
    )
    @has_permissions(administrator=True)
    async def disable_greetings(self, inter: AppCmdInter) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "greetings_enabled",
            False,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command(
        name="greetings_channel",
        description="Установить канал для приветствий",
    )
    @has_permissions(administrator=True)
    async def set_greetings_channel(
        self,
        inter: AppCmdInter,
        channel: TextChannel | None = Param(
            None,
            description="Канал для приветствий. Если пустое - сбросить",
        ),
    ) -> None:
        if not inter.author.guild_permissions.administrator:
            return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "greetings_channel_id",
            channel.id if channel else None,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("GreetingsCog",)
