from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..model import BaseModel
    from ... import BaseAsyncDatabase


class Repository[T: BaseModel](ABC):

    def __init__(self, database: BaseAsyncDatabase, model_cls: type[T]) -> None:
        self._database = database
        self._model_cls = model_cls

    # async def table_size(self, conn: None | Connection = None) -> Decimal:
    #     SQL = f"""
    #         SELECT
    #             ROUND(((data_length + index_length)), 2) AS "size_bytes"
    #         FROM
    #             information_schema.TABLES
    #         WHERE
    #             table_schema = '{self._db.database}'
    #             AND table_name = '{self.table_name}';
    #     """
    #     sql = text(SQL)
    #
    #     res = await self._database.fetch(SQL, connection=conn)
    #     return res[0].get("size_bytes", 0)

    def get_model_cls(self) -> type[T]:
        return self._model_cls

    @property
    def database(self) -> BaseAsyncDatabase:
        return self._database

    async def insert(self, entities: Iterable[T], session: None | AsyncSession = None) -> None:
        async with self.database.must_enter_session(session) as session:
            session.add_all(entities)

    async def create_table(self, session: None | AsyncSession = None) -> None:
        async with self.database.must_enter_session(session) as session:
            conn = await session.connection()
            await conn.run_sync(self.get_model_cls().get_table().create)

    @property
    def table_name(self) -> str:
        return self.get_model_cls().__tablename__
