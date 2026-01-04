""" """

import asyncio
from sys import path

path.append("/livent_bot")
from services.mysqliup import MySqliUp


async def main():
    db = MySqliUp()
    await db.connect()
    await db.begin()
    await db.create_table(
        "guilds",
        {
            "id": "BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY",
            "discord_gid": "BIGINT UNSIGNED UNIQUE NOT NULL",
            "test_option": "INT DEFAULT 1",
        },
    )
    await db.commit()
    await db.close()


asyncio.run(main())
