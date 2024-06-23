from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence, TYPE_CHECKING
import unittest

from sqlalchemy import inspect, select, text

from fazbot import Config
from fazbot.db import fazbot

if TYPE_CHECKING:
    from sqlalchemy import Connection
    from fazbot.db.fazbot.model import BaseModel
    from fazbot.db.fazbot.repository._repository import Repository


class CommonRepositoryTest:
    """Nesting test classes like this prevents CommonRepositoryTest.Test from being run by unittest."""

    class Test[T: BaseModel, ID](unittest.IsolatedAsyncioTestCase, ABC):

        # override
        async def asyncSetUp(self) -> None:
            conf = Config()
            conf.read()
            
            self.database = fazbot.FazBotDatabase(
                "mysql+aiomysql",
                conf.mysql_username,
                conf.mysql_password,
                conf.mysql_host,
                conf.mysql_port,
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
            """Test if insert method() inserts an entry successfully and properly to table."""
            test_data0 = self.test_data[0]

            await self.repo.insert(test_data0)

            rows = await self.__get_all_rows()
            self.assertEqual(len(rows), 1)
            self.assertEqual(str(rows[0]), str(test_data0))

        async def test_insert_successful_many_entries(self) -> None:
            """Test if insert method() inserts many entries successfully and properly to table."""
            await self.repo.insert(self.test_data)

            rows = await self.__get_all_rows()
            self.assertEqual(len(rows), 3)
            self.assertSetEqual(
                set(map(str, rows)),
                set(map(str, self.test_data))
            )

        async def test_delete_successful(self) -> None:
            """Test if delete() method deletes 1 target entry properly."""
            test_data0 = self.test_data[0]
            await self.repo.insert(test_data0)
            id_ = self.__get_value_of_primary_key(test_data0)

            await self.repo.delete(id_)

            rows = await self.__get_all_rows()
            self.assertEqual(len(rows), 0)

        async def test_delete_successful_many_entries(self) -> None:
            """Test if delete() method deletes many target entries properly."""
            await self.repo.insert(self.test_data)
            ids = self.__get_values_of_primary_key(self.test_data)

            await self.repo.delete(ids)

            rows = await self.__get_all_rows()
            self.assertEqual(len(rows), 0)

        async def test_is_exists_return_correct_value(self) -> None:
            """Test if is_exist() method correctly finds if value exists."""
            test_data0 = self.test_data[0]
            await self.repo.insert(test_data0)
            id_ = self.__get_value_of_primary_key(test_data0)

            is_exists = await self.repo.is_exists(id_)
            self.assertTrue(is_exists)

            is_exist2 = await self.repo.is_exists("shouldn't exist")  # type: ignore
            self.assertFalse(is_exist2)

        # override
        async def asyncTearDown(self) -> None:
            await self.database.engine.dispose()
            return await super().asyncTearDown()

        async def __get_all_rows(self) -> Sequence[T]:
            async with self.database.enter_session() as session:
                result = await session.execute(select(self.model_cls))
                rows = result.scalars().all()
            return rows

        def __get_values_of_primary_key(self, entities: Sequence[T]) -> Sequence[ID]:
            pk_columns = inspect(self.repo.get_model_cls()).primary_key
            if len(pk_columns) == 1:
                col_ = pk_columns[0]
                values = [getattr(entity, col_.name) for entity in entities]
                return values
            else:
                values = [getattr(entity, col.name) for col in pk_columns for entity in entities]
                return values

        def __get_value_of_primary_key(self, entity: T) -> ID:
            pk_columns = inspect(self.repo.get_model_cls()).primary_key
            if len(pk_columns) == 1:
                col_ = pk_columns[0]
                value = getattr(entity, col_.name)
                return value
            else:
                values = [getattr(entity, col.name) for col in pk_columns]
                return values  # type: ignore

        @staticmethod
        def __get_table_names(connection: Connection) -> list[str]:
            inspector = inspect(connection)
            return inspector.get_table_names()

        @abstractmethod
        def get_data(self) -> tuple[T, ...]: ...

        @property
        @abstractmethod
        def repo(self) -> Repository[T, ID]: ...
