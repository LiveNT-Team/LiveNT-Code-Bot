from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class GuildSettings(Base):
    __tablename__ = "guilds_settings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    guild_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    greetings_channel_id: Mapped[int] = mapped_column(nullable=True)
    ai_channel_id: Mapped[int] = mapped_column(nullable=True)
    is_greetings_enabled: Mapped[int] = mapped_column(nullable=False, default=False)
    is_ai_enabled: Mapped[int] = mapped_column(nullable=False, default=False)


__all__ = ("GuildSettings",)
