import asyncio
from disnake.ext.commands import Cog, Param, slash_command, InteractionBot
from disnake.errors import Forbidden
from disnake import AppCmdInter, Member, Role, User
from datetime import datetime, timedelta

from core.embeds import (
    YouCannotMentionBotInsteadMemberEmbed,
)
from core.models.ban import Ban
from core.logger import logger
from core.singletones import unlimited
from core.base_embeds import ErrorEmbed, SuccessEmbed, WarningEmbed
from core.embeds import NotEnoughPermissionsEmbed
from core.configuration import CHECK_FOR_BANS_EXPIRATIONS_DELAY, DEFAULT_BAN_DURATION
from services.guilds.service import get_guild, set_guild_setting
from services.mysqliup.service import MySqliUp
from services.users.service import get_or_create_user
from services.guilds.service import get_or_create_guild
from services.bans.service import (
    ban_user,
    get_bans_per_day_count,
    get_expired_bans,
    unban_user,
    get_ban_info,
)
from services.permissions.service import get_member_permissions
from cogs.settings.decorators import has_developer_role
from cogs.bans.views import CreateBanRole


class BansCog(Cog):
    def __init__(self, bot: InteractionBot):
        super().__init__()
        self.bot = bot
        asyncio.get_event_loop().create_task(self.start_checking_for_bans_expirations())

    @slash_command()
    @has_developer_role
    async def enable_bans(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "banning_enabled", True)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def disable_bans(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "banning_enabled", False)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_ban_role(
        self,
        inter: AppCmdInter,
        role: Role | None = Param(
            default=None,
            description="Оставьте пустым для значения по умолчанию",
        ),
    ) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "ban_role_id",
            role.id if role else None,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.bot:
            return
        async with MySqliUp() as db:
            await db.connect()
            guild = await get_guild(
                db,
                member.guild.id,
            )
            if not guild:
                return
            if not guild["banning_enabled"]:
                return
            ban_info = await get_ban_info(
                db,
                uid=member.id,
                gid=member.guild.id,
            )
            if ban_info and ban_info["expires_at"] >= datetime.now():
                ban_role = member.guild.get_role(guild["ban_role_id"])
                if ban_role:
                    await member.add_roles(ban_role)
                else:
                    await member.guild.owner.send(
                        embed=WarningEmbed(
                            description=f"На сервере {member.guild.name} включены баны, но не определена бан роль. Участники могут сбросить бан, перезайдя на сервер."
                        )
                    )

    async def start_checking_for_bans_expirations(self) -> None:
        await asyncio.sleep(CHECK_FOR_BANS_EXPIRATIONS_DELAY.total_seconds())
        await self.check_for_bans_expirations()
        logger.debug("Checked for expired bans")
        await self.start_checking_for_bans_expirations()

    async def check_for_bans_expirations(self) -> None:
        async with MySqliUp() as db:
            await db.connect()
            guilds_ids: list[dict[str, int]] = await db.select_rows(
                "bans",
                ("discord_gid",),
                where="expires_at < %s",
                params=(datetime.now(),),
            )
            if not guilds_ids:
                return
            for guild in guilds_ids:
                guild_obj = await get_guild(db, gid=guild["discord_gid"])
                discord_guild = self.bot.get_guild(guild["discord_gid"])
                if not discord_guild:
                    return
                expired_bans: list[Ban] = await get_expired_bans(
                    db,
                    guild["discord_gid"],
                )
                if not expired_bans:
                    continue
                for expired_ban in expired_bans:
                    await db.delete_row(
                        "bans",
                        where="id = %s",
                        params=(expired_ban["id"]),
                    )
                    await db.commit()
                    if not guild_obj["banning_enabled"]:
                        continue
                    banned_member = discord_guild.get_member(expired_ban["discord_uid"])
                    if not banned_member:
                        continue
                    ban_role = discord_guild.get_role(guild_obj["ban_role_id"])
                    if not ban_role:
                        continue
                    await banned_member.remove_roles(ban_role)

    @slash_command()
    async def ban(
        self,
        inter: AppCmdInter,
        member: User | Member,
        reason: str | None = None,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        months: int = 0,
    ) -> None:
        if member.bot:
            return await inter.response.send_message(
                embed=YouCannotMentionBotInsteadMemberEmbed()
            )
        if member.id == inter.author.id:
            return await inter.response.send_message(
                embed=ErrorEmbed(description="Вы не можете забанить сами себя")
            )
        duration = (
            timedelta(
                days=days,
                hours=hours,
                weeks=weeks + months * 4,
            )
            or DEFAULT_BAN_DURATION
        )
        async with MySqliUp() as db:
            await db.connect()
            guild = await get_or_create_guild(db, inter.guild_id)
            if not guild["banning_enabled"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Баны отключены на этом сервере")
                )
            await get_or_create_user(db, inter.guild_id, inter.author.id)
            await get_or_create_user(db, inter.guild_id, member.id)
            author_permissions = await get_member_permissions(
                guild,
                inter.guild,
                inter.author,
            )
            if isinstance(member, Member):
                member_permissions = await get_member_permissions(
                    guild,
                    inter.guild,
                    member,
                )
                if author_permissions["priority"] <= member_permissions["priority"]:
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description=f"У вас недостаточно прав, чтобы забанить {member.mention}"
                        )
                    )
            # Выполняем проверку на превышение максимальной длительности бана, количества банов выданных сегодня, и саму возможность банить
            if not author_permissions["ban_members"]:
                return await inter.response.send_message(
                    embed=NotEnoughPermissionsEmbed()
                )
            if not author_permissions["max_ban_duration"] is unlimited:
                if duration > author_permissions["max_ban_duration"]:
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description=f"Вы превысили максимальную продолжительность бана для своей роли. Максимальная продолжительность: {author_permissions["max_ban_duration"]}"
                        )
                    )
            if not author_permissions["max_bans_per_day"] is unlimited:
                if (
                    await get_bans_per_day_count(db, inter.author.id)
                    >= author_permissions["max_bans_per_day"]
                ):
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description=f"Вы достигли лимита по количеству банов на сегодня. Максимальное количество банов в день для вашей роли: {author_permissions['max_bans_per_day']}"
                        )
                    )
            # Получаем бан-роль, если бан роль не определена, предложить создать, если автором является пользователь с ролью разработчик или пользователь с правами администратора
            ban_role = inter.guild.get_role(guild["ban_role_id"])
            if not ban_role:
                if (
                    inter.author.guild_permissions.administrator
                    or inter.guild.get_role(guild["developer_role_id"])
                    in inter.author.roles
                ):
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description="Бан роль не определена, создать и определить?"
                        ),
                        view=CreateBanRole(),
                    )
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Бан роль не определена")
                )
            # Выдаём бан и обрабатываем исключения
            try:
                if isinstance(member, Member):
                    await member.add_roles(ban_role)
            except Forbidden:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У бота недостаточно прав, чтобы выдать роль"
                    )
                )
            else:
                await ban_user(
                    db,
                    discord_admin_id=inter.author.id,
                    gid=inter.guild_id,
                    uid=member.id,
                    duration=duration,
                    reason=reason,
                )
                return await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    async def unban(
        self,
        inter: AppCmdInter,
        member: User | Member,
    ) -> None:
        if member.bot:
            return await inter.response.send_message(
                embed=YouCannotMentionBotInsteadMemberEmbed()
            )
        if member.id == inter.author.id:
            return await inter.response.send_message(
                embed=ErrorEmbed(description="Вы не можете разбанить сами себя")
            )
        async with MySqliUp() as db:
            await db.connect()
            guild = await get_or_create_guild(db, inter.guild_id)
            if not guild["banning_enabled"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Баны отключены на этом сервере")
                )
            author_guild_permissions = await get_member_permissions(
                guild_obj=guild,
                discord_guild=inter.guild,
                member=inter.author,
            )
            if not author_guild_permissions:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У вас недостаточно прав, чтобы разбанить этого участника"
                    )
                )
            ban_info = await get_ban_info(
                db,
                gid=inter.guild_id,
                uid=member.id,
            )
            if not ban_info:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Этот участник не забанен")
                )

            if not author_guild_permissions["unban_members"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У вас недостаточно прав чтобы разбанить этого участника"
                    )
                )
            admin = inter.guild.get_member(ban_info["discord_admin_id"])
            if admin:
                admin_guild_permissions = await get_member_permissions(
                    guild_obj=guild,
                    discord_guild=inter.guild,
                    member=admin,
                )
                if admin_guild_permissions:
                    if (
                        admin_guild_permissions["priority"]
                        > author_guild_permissions["priority"]
                    ):
                        return await inter.response.send_message(
                            embed=ErrorEmbed(
                                description="Вы не можете разбанить этого участника, так как он был забанен администратором с более высоким приоритетом"
                            )
                        )
            if isinstance(member, Member):
                ban_role = inter.guild.get_role(guild["ban_role_id"])
                if not ban_role:
                    if not inter.author.guild_permissions.administrator:
                        developer_role = inter.guild.get_role(
                            guild["developer_role_id"]
                        )
                        if developer_role and developer_role in inter.author.roles:
                            return await inter.response.send_message(
                                embed=ErrorEmbed(
                                    description="Бан роль не определена, создать и определить?"
                                ),
                                view=CreateBanRole(),
                            )
                    return await inter.response.send_message(
                        embed=ErrorEmbed(description="Бан роль не определена")
                    )
                await member.remove_roles(ban_role)
            await unban_user(
                db,
                gid=inter.guild_id,
                uid=member.id,
            )
            await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("BansCog",)
