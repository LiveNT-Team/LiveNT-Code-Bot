import datetime
from typing import TypedDict


class Mut(TypedDict):
    id: int
    discord_admin_id: int
    discord_uid: int
    discord_gid: int
    expires_at: datetime
    created_at: datetime
    reason: str
