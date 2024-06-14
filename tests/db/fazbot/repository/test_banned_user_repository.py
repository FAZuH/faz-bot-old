import asyncio
from datetime import datetime, timedelta
from typing import Any
import unittest

from aiomysql import IntegrityError

from fazbot.db import DatabaseQuery
from fazbot.db.fazbot.model import BannedUser, banned_user
from fazbot.db.fazbot.repository import BannedUserRepository


class TestBannedUserRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.e_userid1 = 12345
        self.e_userid2 = 12346
        self.e_reason = 'test'
        self.e_from = datetime.now()
        self.e_until = datetime.now() + timedelta(days=1)
        self.e_untilnone = None

        self.entity1 = BannedUser(self.e_userid1, self.e_reason, self.e_from, self.e_until)
        self.entity2 = BannedUser(self.e_userid2, self.e_reason, self.e_from, self.e_untilnone)
        self.entity3 = BannedUser(self.e_userid2, self.e_reason, self.e_from, self.e_until)

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
        cls.eventloop = asyncio.new_event_loop()
        cls.eventloop.run_until_complete(cls.repo.create_table())
        cls.eventloop.run_until_complete(cls.__truncate())

    async def test_create_table(self) -> None:
        # ACT
        await self.repo.create_table()

        # ASSERT
        results = await self.db.fetch("SHOW TABLES")
        table_names = []
        for result in results:
            table_name = list(result.values())
            table_names.extend(table_name)

        self.assertIn(self.repo.TABLE_NAME, table_names)

    async def test_add(self) -> None:
        # ACT
        await self.repo.insert(self.entity1)
        await self.repo.insert(self.entity2)
        
        # ASSERT
        results = await self.__select_all()
        self.assertEqual(len(results), 2)

        entity1id = BannedUser.from_dict(results[0]).user_id
        entity2id = BannedUser.from_dict(results[1]).user_id

        self.assertSetEqual({entity1id, entity2id}, {self.e_userid1, self.e_userid2})

    async def test_remove(self) -> None:
        # PREPARE
        await self.repo.insert(self.entity1)

        # ACT
        await self.repo.delete(self.e_userid1)

        # ASSERT
        results = await self.__select_all()
        self.assertEqual(len(results), 0)

    async def test_find(self) -> None:
        # PREPARE
        await self.repo.insert(self.entity1)

        # ACT
        entity1 = await self.repo.find_one(self.e_userid1)
        
        # ASSERT
        self.assertEqual(entity1.user_id, self.entity1.user_id)  # type: ignore

    async def test_find_all(self) -> None:
        # PREPARE
        await self.repo.insert(self.entity1)
        await self.repo.insert(self.entity2)
        userids = [self.e_userid1, self.e_userid2]

        # ACT
        entities = await self.repo.find_all(userids)

        # ASSERT
        for entity in entities:
            self.assertIn(entity.user_id, userids)

    async def test_exists(self) -> None:
        # PREPARE
        await self.repo.insert(self.entity1)

        # ACT
        isexists = await self.repo.is_exists(self.e_userid1)
        self.assertTrue(isexists)

    async def test_primary_constraint(self) -> None:
        # ACT
        with self.assertRaises(IntegrityError):
            await self.repo.insert(self.entity2)
            await self.repo.insert(self.entity3)

    async def asyncTearDown(self) -> None:
        await self.__truncate()
        return await super().asyncTearDown()

    @classmethod
    async def __truncate(cls) -> None:
        await cls.db.execute(f"TRUNCATE {cls.repo.TABLE_NAME}")
    
    async def __select_all(self) -> list[dict[str, Any]]:
        results = await self.db.fetch(f" SELECT * FROM {self.repo.TABLE_NAME}")
        return results
