from typing import TypedDict
from datetime import datetime


class User(TypedDict):
    id: int
    discord_gid: int
    discord_uid: int
    ai_per_name: str
    messages_count: int
