from sqlalchemy import BIGINT
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class GuildSettings(Base):
    __tablename__ = "guilds_settings"
    guild_id: Mapped[int] = mapped_column(
        BIGINT(),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    greetings_channel_id: Mapped[int] = mapped_column(BIGINT(), nullable=True)
    ai_channel_id: Mapped[int] = mapped_column(BIGINT(), nullable=True)
    activist_role_id: Mapped[int] = mapped_column(BIGINT(), nullable=True)
    developer_role_id: Mapped[int] = mapped_column(BIGINT(), nullable=True)
    activist_role_messages_count: Mapped[int] = mapped_column(nullable=True)
    """Сколько сообщений надо отправить чтобы получить роль активиста"""
    is_greetings_enabled: Mapped[bool] = mapped_column(default=False)
    is_ai_enabled: Mapped[bool] = mapped_column(default=False)
    is_activist_role_extraditing: Mapped[bool] = mapped_column(default=False)


__all__ = ("GuildSettings",)
