import datetime
from typing import TypedDict


class Ban(TypedDict):
    id: int
    discord_uid: int
    discord_gid: int
    expires_at: datetime
    reason: str
