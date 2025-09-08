from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import VARCHAR, BIGINT

from .base import Base
from ...core.configuration import DEFAULT_PERSONALITY_NAME


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, index=True)
    discord_id: Mapped[int] = mapped_column(BIGINT(), nullable=False, unique=True)
    guild_id: Mapped[int] = mapped_column(BIGINT(), nullable=False)
    messages_count: Mapped[int] = mapped_column(nullable=False, default=0)
    current_personality_name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False, default=DEFAULT_PERSONALITY_NAME)


__all__ = ("User",)
