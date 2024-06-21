from __future__ import annotations
from abc import ABC
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable

from sqlalchemy import Column, delete, inspect, text, select, exists

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..model import BaseModel
    from ... import BaseAsyncDatabase


class Repository[T: BaseModel](ABC):

    def __init__(self, database: BaseAsyncDatabase, model_cls: type[T]) -> None:
        self._database = database
        self._model_cls = model_cls

    async def table_disk_usage(self, session: None | AsyncSession = None) -> Decimal:
        """
        Calculate the size of the table in bytes.

        Parameters
        ----------
        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        Decimal
            Size of the table in bytes.
        """
        SQL = f"""
            SELECT
                ROUND(((data_length + index_length)), 2) AS "size_bytes"
            FROM
                information_schema.TABLES
            WHERE
                table_schema = :schema
                AND table_name = :table_name;
        """
        params = {
            "schema": self._database.database,
            "table_name": self.table_name
        }
        async with self._database.must_enter_session(session) as session:
            result = await session.execute(text(SQL), params)
            row = result.fetchone()
            ret = Decimal(row["size_bytes"]) if (row and row["size_bytes"] is not None) else Decimal(0)  # type: ignore
            return ret

    async def create_table(self, session: None | AsyncSession = None) -> None:
        fn = lambda conn: self.get_model_cls().get_table().create(conn, checkfirst=True)
        async with self.database.must_enter_session(session) as session:
            conn = await session.connection()
            await conn.run_sync(fn)

    async def insert(self, entities: Iterable[T] | T, session: None | AsyncSession = None) -> None:
        iterable = self.__ensure_iterable(entities)
        async with self.database.must_enter_session(session) as session:
            session.add_all(iterable)

    async def delete(self, id_: Any, session: AsyncSession | None = None) -> None:
        """Deletes an entry from the repository based on `id_`

        Parameters
        ----------
        id_: Any
            Primary_key value of the entry to delete.

        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        model = self.get_model_cls()
        async with self.database.must_enter_session(session) as session:
            stmt = (
                delete(model).
                where(self.__get_primary_key() == id_)
            )
            await session.execute(stmt)

    def get_model_cls(self) -> type[T]:
        return self._model_cls

    @property
    def database(self) -> BaseAsyncDatabase:
        return self._database

    @property
    def table_name(self) -> str:
        return self.get_model_cls().__tablename__

    def __get_primary_key(self) -> Column[Any]:
        model_cls = self.get_model_cls()
        primary_key_name = inspect(model_cls).primary_key[0]
        # primary_key_variable = getattr(model_cls, primary_key_name)
        return primary_key_name

    @staticmethod
    def __ensure_iterable[U](obj: Iterable[U] | U) -> Iterable[U]:
        if isinstance(obj, Iterable):
            return obj
        else:
            return (obj,)
