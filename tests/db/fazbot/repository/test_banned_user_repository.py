import asyncio
import unittest

from fazbot.db import DatabaseQuery
from fazbot.db.fazbot.repository import BannedUserRepository


class TestBannedUserRepository(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = DatabaseQuery(
            "localhost",
            "test",
            "test",
            "test_fazbot",
            retries=3
        )
        cls.repo = BannedUserRepository(cls.db)
        eventloop = asyncio.new_event_loop()
        eventloop.run_until_complete(cls.repo.create_table())

    async def test_create_table(self) -> None:
        # ACT
        await self.repo.create_table()

        # ASSERT
        table = (await self.db.fetch("SHOW TABLES"))[0]
        tablenames = list(table.values())
        self.assertIn(self.repo.TABLE_NAME, tablenames)

