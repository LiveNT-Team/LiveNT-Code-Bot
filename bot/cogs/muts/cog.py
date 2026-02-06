import asyncio
from disnake.ext.commands import Cog, Param, slash_command, InteractionBot
from disnake.errors import Forbidden
from disnake import AppCmdInter, Member, Role, User
from datetime import datetime, timedelta

from core.models.mut import Mut
from core.logger import logger
from core.singletones import unlimited
from core.base_embeds import ErrorEmbed, SuccessEmbed, WarningEmbed
from core.embeds import NotEnoughPermissionsEmbed, YouCannotMentionBotInsteadMemberEmbed
from core.configuration import CHECK_FOR_MUTS_EXPIRATIONS_DELAY, DEFAULT_MUT_DURATION
from services.guilds.service import get_guild, set_guild_setting
from services.mysqliup.service import MySqliUp
from services.users.service import get_or_create_user
from services.guilds.service import get_or_create_guild
from services.muts.service import (
    mute_user,
    get_muts_per_day_count,
    unmute_user,
    get_mut_info,
    get_expired_muts,
)
from services.permissions.service import get_member_permissions
from cogs.settings.decorators import has_developer_role
from cogs.muts.views import CreateMutRole


class MutsCog(Cog):
    def __init__(self, bot: InteractionBot):
        super().__init__()
        self.bot = bot
        asyncio.get_event_loop().create_task(self.start_checking_for_muts_expirations())

    @slash_command()
    @has_developer_role
    async def enable_muts(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "muting_enabled", True)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def disable_muts(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "muting_enabled", False)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_mut_role(
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
            "mut_role_id",
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
            if not guild["muting_enabled"]:
                return
            mut_info = await get_mut_info(
                db,
                uid=member.id,
                gid=member.guild.id,
            )
            if mut_info and mut_info["expires_at"] >= datetime.now():
                mut_role = member.guild.get_role(guild["mut_role_id"])
                if mut_role:
                    await member.add_roles(mut_role)
                else:
                    await member.guild.owner.send(
                        embed=WarningEmbed(
                            description=f"На сервере {member.guild.name} включены муты, но не определена мьют роль. Участники могут сбросить мьют, перезайдя на сервер."
                        )
                    )

    async def start_checking_for_muts_expirations(self) -> None:
        await asyncio.sleep(CHECK_FOR_MUTS_EXPIRATIONS_DELAY.total_seconds())
        await self.check_for_muts_expirations()
        logger.debug("Checked for expired muts")
        await self.start_checking_for_muts_expirations()

    async def check_for_muts_expirations(self) -> None:
        async with MySqliUp() as db:
            await db.connect()
            guilds_ids: list[dict[str, int]] = await db.select_rows(
                "muts",
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
                expired_bans: list[Mut] = await get_expired_muts(
                    db,
                    guild["discord_gid"],
                )
                if not expired_bans:
                    continue
                for expired_ban in expired_bans:
                    await db.delete_row(
                        "muts",
                        where="id = %s",
                        params=(expired_ban["id"]),
                    )
                    await db.commit()
                    if not guild_obj["muting_enabled"]:
                        continue
                    muted_member = discord_guild.get_member(expired_ban["discord_uid"])
                    if not muted_member:
                        continue
                    mut_role = discord_guild.get_role(guild_obj["mut_role_id"])
                    if not mut_role:
                        continue
                    await muted_member.remove_roles(mut_role)

    @slash_command()
    async def mute(
        self,
        inter: AppCmdInter,
        member: User | Member,
        reason: str | None = None,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> None:
        if member.bot:
            return await inter.response.send_message(
                embed=YouCannotMentionBotInsteadMemberEmbed()
            )
        if member.id == inter.author.id:
            return await inter.response.send_message(
                embed=ErrorEmbed(description="Вы не можете замьютить сами себя")
            )
        duration = (
            timedelta(
                seconds=seconds,
                minutes=minutes,
                days=days,
                hours=hours,
            )
            or DEFAULT_MUT_DURATION
        )
        async with MySqliUp() as db:
            await db.connect()
            guild = await get_or_create_guild(db, inter.guild_id)
            if not guild["muting_enabled"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Муты отключены на этом сервере")
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
                            description=f"У вас недостаточно прав, чтобы замутить {member.mention}"
                        )
                    )
            # Выполняем проверку на превышение максимальной длительности мьюта, количества мьютов выданных сегодня, и саму возможность мьютить
            if not author_permissions["mute_members"]:
                return await inter.response.send_message(
                    embed=NotEnoughPermissionsEmbed()
                )
            if not author_permissions["max_mut_duration"] is unlimited:
                if duration > author_permissions["max_mut_duration"]:
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description=f"Вы превысили максимальную продолжительность мьюта для своей роли. Максимальная продолжительность: {author_permissions["max_mut_duration"]}"
                        )
                    )
            if not author_permissions["max_muts_per_day"] is unlimited:
                if (
                    await get_muts_per_day_count(db, inter.author.id)
                    >= author_permissions["max_muts_per_day"]
                ):
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description=f"Вы достигли лимита по количеству мьютов на сегодня. Максимальное количество мьютов в день для вашей роли: {author_permissions['max_muts_per_day']}"
                        )
                    )
            # Получаем мьют-роль, если бан роль не определена, предложить создать, если автором является пользователь с ролью разработчик или пользователь с правами администратора
            mut_role = inter.guild.get_role(guild["mut_role_id"])
            if not mut_role:
                if (
                    inter.author.guild_permissions.administrator
                    or inter.guild.get_role(guild["developer_role_id"])
                    in inter.author.roles
                ):
                    return await inter.response.send_message(
                        embed=ErrorEmbed(
                            description="Мьют роль не определена, создать и определить?"
                        ),
                        view=CreateMutRole(),
                    )
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Мьют роль не определена")
                )
            # Выдаём мьют и обрабатываем исключения
            try:
                if isinstance(member, Member):
                    await member.add_roles(mut_role)
            except Forbidden:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У бота недостаточно прав, чтобы выдать роль"
                    )
                )
            else:
                await mute_user(
                    db,
                    discord_admin_id=inter.author.id,
                    gid=inter.guild_id,
                    uid=member.id,
                    duration=duration,
                    reason=reason,
                )
                return await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    async def unmute(
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
                embed=ErrorEmbed(description="Вы не можете размьютить сами себя")
            )
        async with MySqliUp() as db:
            await db.connect()
            guild = await get_or_create_guild(db, inter.guild_id)
            if not guild["muting_enabled"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Мьюты отключены на этом сервере")
                )
            author_guild_permissions = await get_member_permissions(
                guild_obj=guild,
                discord_guild=inter.guild,
                member=inter.author,
            )
            if not author_guild_permissions:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У вас недостаточно прав, чтобы размьютить этого участника"
                    )
                )
            mut_info = await get_mut_info(
                db,
                gid=inter.guild_id,
                uid=member.id,
            )
            if not mut_info:
                return await inter.response.send_message(
                    embed=ErrorEmbed(description="Этот участник не замьючен")
                )

            if not author_guild_permissions["unmute_members"]:
                return await inter.response.send_message(
                    embed=ErrorEmbed(
                        description="У вас недостаточно прав чтобы размьютить этого участника"
                    )
                )
            admin = inter.guild.get_member(mut_info["discord_admin_id"])
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
                                description="Вы не можете размьютить этого участника, так как он был замьючен администратором с более высоким приоритетом"
                            )
                        )
            if isinstance(member, Member):
                mut_role = inter.guild.get_role(guild["mut_role_id"])
                if not mut_role:
                    if not inter.author.guild_permissions.administrator:
                        developer_role = inter.guild.get_role(
                            guild["developer_role_id"]
                        )
                        if developer_role and developer_role in inter.author.roles:
                            return await inter.response.send_message(
                                embed=ErrorEmbed(
                                    description="Мут роль не определена, создать и определить?"
                                ),
                                view=CreateMutRole(),
                            )
                    return await inter.response.send_message(
                        embed=ErrorEmbed(description="Мут роль не определена")
                    )
                await member.remove_roles(mut_role)
            await unmute_user(
                db,
                gid=inter.guild_id,
                uid=member.id,
            )
            await inter.response.send_message(embed=SuccessEmbed())


__all__ = ("BansCog",)
