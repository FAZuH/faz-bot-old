from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
import unittest

from sqlalchemy import inspect, select, text

from fazbot.db import fazbot

if TYPE_CHECKING:
    from sqlalchemy import Connection
    from fazbot.db.fazbot.model import BaseModel
    from fazbot.db.fazbot.repository._repository import Repository


class CommonRepositoryTest:
    """Nesting test classes like this prevents CommonRepositoryTest.Test from being run by unittest."""

    class Test[T: BaseModel, ID](ABC, unittest.IsolatedAsyncioTestCase):

        # override
        async def asyncSetUp(self) -> None:
            self.database = fazbot.FazBotDatabase(
                "mysql+aiomysql",
                "fazbot",
                "password",
                "localhost",
                "fazbot_test"
            )
            async with self.database.enter_session() as session:
                await self.repo.create_table(session)
                await session.execute(text(f"TRUNCATE TABLE {self.repo.table_name}"))

            self.model_cls = self.repo.get_model_cls()
            self.test_data = self.get_data()
            return await super().asyncSetUp()

        async def test_create_table_successful(self) -> None:
            """Test if create_table() method successfully creates table."""
            await self.repo.create_table()

            async with self.database.enter_connection() as connection:
                result = await connection.run_sync(self.__get_table_names)

            self.assertTrue(self.repo.table_name in result)

        async def test_insert_successful(self) -> None:
            """Test if insert method() inserts entries successfully and properly to table."""
            await self.repo.insert(self.test_data)

            async with self.database.enter_session() as session:
                result = await session.execute(select(self.model_cls))
                rows = result.scalars().all()

            self.assertEqual(len(rows), 1)
            self.assertEqual(str(rows[0]), str(self.test_data))

        async def test_delete_successful(self) -> None:
            """Test if delete() method deletes target entry properly."""
            await self.repo.insert(self.test_data)

            await self.repo.delete(self.primary_key_value)

            async with self.database.enter_session() as session:
                result = await session.execute(select(self.model_cls))
                rows = result.scalars().all()

            self.assertEqual(len(rows), 0)

        async def test_is_exists_return_correct_value(self) -> None:
            """Test if is_exist() method correctly finds if value exists."""
            await self.repo.insert(self.test_data)

            is_exists = await self.repo.is_exists(self.primary_key_value)
            
            self.assertTrue(is_exists)

            is_exist2 = await self.repo.is_exists("shouldn't exist")  # type: ignore

            self.assertFalse(is_exist2)

        # override
        async def asyncTearDown(self) -> None:
            await self.database.engine.dispose()
            return await super().asyncTearDown()

        @staticmethod
        def __get_table_names(connection: Connection) -> list[str]:
            inspector = inspect(connection)
            return inspector.get_table_names()

        @abstractmethod
        def get_data(self) -> T: ...

        @property
        @abstractmethod
        def repo(self) -> Repository[T, ID]: ...

        @property
        @abstractmethod
        def primary_key_value(self) -> Any: ...
