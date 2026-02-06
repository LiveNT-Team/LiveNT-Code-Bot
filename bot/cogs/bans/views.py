from disnake import MessageInteraction, Permissions
from disnake.ui import View, button, Button

from core.base_embeds import SuccessEmbed
from services.guilds.service import set_guild_setting
from services.mysqliup.service import MySqliUp


class CreateBanRole(View):
    def __init__(self):
        super().__init__(timeout=30)

    @button(label="Создать роль")
    async def create_ban_role_callback(
        self,
        button: Button,
        inter: MessageInteraction,
    ) -> None:
        ban_role = await inter.guild.create_role(
            name="BANNED",
            permissions=Permissions(),
        )
        async with MySqliUp() as db:
            await db.connect()
            await set_guild_setting(
                db,
                gid=inter.guild_id,
                name="ban_role_id",
                value=ban_role.id,
            )
            await db.commit()
        await inter.response.send_message(
            embed=SuccessEmbed(description=f"Бан роль создана: {ban_role.mention}")
        )
