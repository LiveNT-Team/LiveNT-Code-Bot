from disnake.ext.commands import Cog, Param, slash_command, has_permissions
from disnake import AppCmdInter, Role, TextChannel

from services.guilds.service import get_or_create_guild, set_guild_setting
from services.mysqliup.service import MySqliUp
from core.base_embeds import InfoEmbed, SuccessEmbed
from core.embeds import NotEnoughPermissionsEmbed
from .decorators import has_developer_role


class SettingsCog(Cog):
	@slash_command()
	async def set(self, inter: AppCmdInter) -> None:
		pass

	@slash_command()
	async def get(self, inter: AppCmdInter) -> None:
		pass

	@slash_command()
	async def enable(self, inter: AppCmdInter) -> None:
		pass

	@slash_command()
	async def disable(self, inter: AppCmdInter) -> None:
		pass

	@slash_command(description="Выводит настройки бота для этого сервера")
	@has_developer_role
	async def get_settings(self, inter: AppCmdInter) -> None:
		db = MySqliUp()
		await db.connect()
		await db.begin()
		guild = await get_or_create_guild(db, inter.guild_id)
		await db.commit()
		await db.close()
		settings_embed = InfoEmbed()
		settings_embed.add_field(
			"Роль разработчика",
			(
				f"<@&{guild['developer_role_id']}>"
				if guild["developer_role_id"]
				else "Не задана"
			),
		)
		settings_embed.add_field(
			"Приветствия",
			"Включены" if guild["greetings_enabled"] else "Выключены",
		)
		settings_embed.add_field(
			"Канал приветствий",
			(
				f"<#{guild['greetings_channel_id']}>"
				if guild["greetings_channel_id"]
				else "Не задан"
			),
		)
		await inter.response.send_message(embed=settings_embed, ephemeral=True)

	@slash_command("set_developer_role", "Изменение роли разработчика")
	@has_permissions(administrator=True)
	async def set_developer_role(
		self,
		inter: AppCmdInter,
		new_role: Role | None = Param(
			None,
			description="Новое значение для параметра. Если пустое - значение по умолчанию",
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
			"developer_role_id",
			new_role.id if new_role else None,
		)
		await db.commit()
		await db.close()
		await inter.response.send_message(embed=SuccessEmbed())

	@enable.sub_command(description="Включить приветствия")
	@has_permissions(administrator=True)
	async def greetings(self, inter: AppCmdInter) -> None:
		if not inter.author.guild_permissions.administrator:
			return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
		db = MySqliUp()
		await db.connect()
		await db.begin()
		await set_guild_setting(db, inter.guild_id, "greetings_enabled", True)
		await db.commit()
		await db.close()
		await inter.response.send_message(embed=SuccessEmbed())

	@disable.sub_command(name="greetings", description="Выключить приветствия")
	@has_permissions(administrator=True)
	async def disable_greetings(self, inter: AppCmdInter) -> None:
		if not inter.author.guild_permissions.administrator:
			return await inter.response.send_message(embed=NotEnoughPermissionsEmbed())
		db = MySqliUp()
		await db.connect()
		await db.begin()
		await set_guild_setting(db, inter.guild_id, "greetings_enabled", False)
		await db.commit()
		await db.close()
		await inter.response.send_message(embed=SuccessEmbed())

	@set.sub_command(name="greetings_channel", description="Установить канал для приветствий")
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
		await set_guild_setting(db, inter.guild_id, "greetings_channel_id", channel.id if channel else None)
		await db.commit()
		await db.close()
		await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("SettingsCog",)
