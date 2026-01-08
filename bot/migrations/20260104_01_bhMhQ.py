import asyncio
from sys import path

path.append("/livent_bot")
from services.mysqliup import MySqliUp


__depends__ = {"20260103_01_d2FeD"}


async def main():
    db = MySqliUp()
    await db.connect()
    await db.begin()
    await db.delete_column("guilds", "test_option")
    await db.create_column(
        "guilds",
        "developer_role_id",
        "INT UNSIGNED NULL DEFAULT NULL",
    )
    await db.commit()
    await db.close()


asyncio.run(main())
