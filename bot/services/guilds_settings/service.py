from typing import Optional, Dict, Any
from ..mysqliup import MySqliUp


class GuildSettingsService:
    TABLE_NAME = "guild_settings"

    def __init__(self, db: MySqliUp):
        self.db = db

    async def ensure_table_exists(self) -> None:
        await self.db.create_table(
            self.TABLE_NAME,
            {
                "guild_id": "BIGINT UNSIGNED PRIMARY KEY",
                "is_greetings_enabled": "TINYINT(1) DEFAULT 0",
                "greetings_channel_id": "BIGINT UNSIGNED DEFAULT NULL",
                "is_ai_enabled": "TINYINT(1) DEFAULT 0",
                "ai_channel_id": "BIGINT UNSIGNED DEFAULT NULL",
                "developer_role_id": "BIGINT UNSIGNED DEFAULT NULL",
                "activist_role_id": "BIGINT UNSIGNED DEFAULT NULL",
                "activist_role_messages_count": "INT UNSIGNED DEFAULT 0",
                "is_activist_role_extraditing": "TINYINT(1) DEFAULT 0",
            },
        )

    async def get_or_create(self, guild_id: int) -> Dict[str, Any]:
        existing = await self.db.select_all_row(
            self.TABLE_NAME, "guild_id = %s", (guild_id,)
        )

        if existing:
            return existing

        await self.db.create_row(
            self.TABLE_NAME,
            {
                "guild_id": guild_id,
                "is_greetings_enabled": 0,
                "greetings_channel_id": None,
                "is_ai_enabled": 0,
                "ai_channel_id": None,
                "developer_role_id": None,
                "activist_role_id": None,
                "activist_role_messages_count": 0,
                "is_activist_role_extraditing": 0,
            },
        )

        return await self.db.select_all_row(
            self.TABLE_NAME, "guild_id = %s", (guild_id,)
        )

    async def enable_greetings(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"is_greetings_enabled": 1},
            "guild_id = %s",
            (guild_id,),
        )

    async def disable_greetings(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"is_greetings_enabled": 0},
            "guild_id = %s",
            (guild_id,),
        )

    async def set_greetings_channel(self, guild_id: int, channel_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"greetings_channel_id": channel_id},
            "guild_id = %s",
            (guild_id,),
        )

    async def enable_ai(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME, {"is_ai_enabled": 1}, "guild_id = %s", (guild_id,)
        )

    async def disable_ai(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME, {"is_ai_enabled": 0}, "guild_id = %s", (guild_id,)
        )

    async def set_ai_channel(self, guild_id: int, channel_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"ai_channel_id": channel_id},
            "guild_id = %s",
            (guild_id,),
        )

    async def set_developer_role(self, guild_id: int, role_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"developer_role_id": role_id},
            "guild_id = %s",
            (guild_id,),
        )

    async def set_activist_role(self, guild_id: int, role_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"activist_role_id": role_id},
            "guild_id = %s",
            (guild_id,),
        )

    async def set_activist_messages_count(
        self, guild_id: int, count: int
    ) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"activist_role_messages_count": count},
            "guild_id = %s",
            (guild_id,),
        )

    async def enable_activist_extraditing(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"is_activist_role_extraditing": 1},
            "guild_id = %s",
            (guild_id,),
        )

    async def disable_activist_extraditing(self, guild_id: int) -> None:
        await self.get_or_create(guild_id)
        await self.db.update_row(
            self.TABLE_NAME,
            {"is_activist_role_extraditing": 0},
            "guild_id = %s",
            (guild_id,),
        )


_db_instance: Optional[MySqliUp] = None


async def init_guild_settings(db: MySqliUp) -> None:
    global _db_instance
    _db_instance = db
    service = GuildSettingsService(db)
    await service.ensure_table_exists()


async def get_or_create_guild_settings(guild_id: int) -> Dict[str, Any]:
    if _db_instance is None:
        raise RuntimeError("Сервис не инициализирован")
    service = GuildSettingsService(_db_instance)
    return await service.get_or_create(guild_id)
