from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import VARCHAR, BIGINT

from .base import Base
from ...core.configuration import DEFAULT_PERSONALITY_NAME


class User(Base):
    __tablename__ = "users"
    discord_id: Mapped[int] = mapped_column(BIGINT(), nullable=False, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BIGINT(), nullable=False)
    messages_count: Mapped[int] = mapped_column(nullable=False, default=0)
    current_personality_name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False, default=DEFAULT_PERSONALITY_NAME)

    __table_args__ = (
        UniqueConstraint('discord_id', 'guild_id', name='uq_discord_id_guild_id'),
    )

__all__ = ("User",)
