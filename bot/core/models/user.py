from typing import TypedDict
from datetime import datetime


class User(TypedDict):
    id: int
    discord_gid: int
    discord_uid: int
    ai_per_name: str
    banned: bool
    ban_expires_at: datetime
    ban_reason: str
    muted: bool
    mut_expires_at: datetime
    mut_reason: str
