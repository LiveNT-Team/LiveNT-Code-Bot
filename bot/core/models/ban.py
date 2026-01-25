import datetime
from typing import TypedDict


class Ban(TypedDict):
    id: int
    user_id: int
    expires_at: datetime
    reason: str
