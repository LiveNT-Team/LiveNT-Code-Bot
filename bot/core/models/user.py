from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    guild_id: Mapped[int] = mapped_column(nullable=False)
    messages_count: Mapped[int] = mapped_column(nullable=False, default=0)
