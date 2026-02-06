from datetime import timedelta
from typing import TypedDict


class Permissions(TypedDict):
    priority: int
    ban_members: bool
    unban_members: bool
    mute_members: bool
    unmute_members: bool
    max_bans_per_day: int
    max_muts_per_day: int
    max_ban_duration: timedelta
    max_mut_duration: timedelta
