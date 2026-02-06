import disnake
from typing import OrderedDict
from core.models.guild import Guild
from core.models.permissions import Permissions
from core.permissions_list import permissions_list


async def get_member_permissions(
    guild_obj: Guild,
    discord_guild: disnake.Guild,
    member: disnake.Member,
) -> Permissions:
    for role_name, role_id in OrderedDict(
        {
            "main_admin": guild_obj["main_admin_role_id"],
            "major_admin": guild_obj["major_admin_role_id"],
            "admin": guild_obj["admin_role_id"],
            "minor_admin": guild_obj["minor_admin_role_id"],
            "main_moder": guild_obj["main_moder_role_id"],
            "major_moder": guild_obj["major_moder_role_id"],
            "moder": guild_obj["moder_role_id"],
            "minor_moder": guild_obj["minor_moder_role_id"],
        }
    ).items():
        role = discord_guild.get_role(role_id)
        if not role:
            continue
        if not role in member.roles:
            continue
        return permissions_list[role_name]
    return permissions_list["member"]
