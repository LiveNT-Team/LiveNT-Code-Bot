from typing import TypedDict


class User(TypedDict):
    id: int
    discord_gid: int
    discord_uid: int
    ai_per_name: str
