from __future__ import annotations
from abc import ABC
from decimal import Decimal
from typing import Any, Iterable, Sequence, TYPE_CHECKING

from sqlalchemy import Column, Tuple, select, text, tuple_
from sqlalchemy.dialects.mysql import insert

if TYPE_CHECKING:
    from sqlalchemy import Table
    from sqlalchemy.ext.asyncio import AsyncSession
    from ._base_mysql_database import BaseMySQLDatabase
    from ._base_model import BaseModel


class BaseRepository[T: BaseModel, ID](ABC):

    def __init__(self, database: BaseMySQLDatabase, model_cls: type[T]) -> None:
        self._database = database
        self._model_cls = model_cls

    async def table_disk_usage(self, *, session: None | AsyncSession = None) -> Decimal:
        """Calculate the size of the table in bytes.

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
            "schema": self._database.async_engine.url.database,
            "table_name": self.table_name
        }

        async with self._database.must_enter_async_session(session) as session:
            result = await session.execute(text(SQL), params)

        row = result.fetchone()
        ret = Decimal(row["size_bytes"]) if (row and row["size_bytes"] is not None) else Decimal(0)  # type: ignore
        return ret

    async def create_table(self) -> None:
        """Create the table associated with the repository if it does not already exist."""
        self.table.create(self.database.engine, checkfirst=True)

    async def insert(
        self,
        entity: Iterable[T] | T,
        *,
        session: None | AsyncSession = None,
        ignore_on_duplicate: bool = False,
        replace_on_duplicate: bool = False,
        columns_to_replace: Iterable[str] | None = None
    ) -> None:
        """Insert one or more entities into the database.

        Parameters
        ----------
        entity : Iterable[T] | T
            An entity or an iterable of entities to be inserted into the database.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        if ignore_on_duplicate and replace_on_duplicate:
            raise ValueError("ignore_on_duplicate and replace_on_duplicate cannot be both True")

        entities = self._ensure_iterable(entity)

        if not ignore_on_duplicate and not replace_on_duplicate:
            async with self.database.must_enter_async_session(session) as session:
                session.add_all(entities)
            return

        entities_dict = [e.to_dict(actual_column_names=False) for e in entities]
        stmt = insert(self.table).values(entities_dict)

        if replace_on_duplicate:
            if columns_to_replace is None:
                columns_to_replace = [c.name for c in self.table.c if not c.primary_key]
            update_cols = {c: getattr(stmt.inserted, c) for c in columns_to_replace}
            stmt = stmt.on_duplicate_key_update(**update_cols)

        if ignore_on_duplicate:
            stmt = stmt.prefix_with("IGNORE")

        async with self.database.must_enter_async_session(session) as session:
            await session.execute(stmt)

    async def delete(self, id_: ID | list[ID], *, session: AsyncSession | None = None) -> None:
        """Deletes an entry from the repository based on `id_`

        Parameters
        ----------
        id_: Any
            Primary_key value of the entry to delete.

        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        primary_keys = self._get_primary_key()
        stmt = self.table.delete().where(primary_keys == id_)
        async with self.database.must_enter_async_session(session) as session:
            await session.execute(stmt)

    async def delete_many(self, id_: list[ID], *, session: AsyncSession | None = None) -> None:
        """Deletes an entry from the repository based on `id_`

        Parameters
        ----------
        id_: Any
            Primary_key value of the entry to delete.

        conn : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        primary_keys = self._get_primary_key()
        stmt = self.table.delete().where(primary_keys.in_(id_))
        async with self.database.must_enter_async_session(session) as session:
            await session.execute(stmt)

    async def is_exists(self, id_: ID, *, session: None | AsyncSession = None) -> bool:
        """Check if an entry with the given primary key exists in the database.

        Parameters
        ----------
        id_ : ID
            Primary key value of the entry to check.
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.

        Returns
        -------
        bool
            True if the entry exists, False otherwise.
        """
        res = await self.select(id_, session=session)
        return res is not None

    async def truncate(self, *, session: None | AsyncSession = None) -> None:
        """Truncates the table.

        Parameters
        ----------
        session : AsyncSession, optional
            Optional AsyncSession object to use for the database connection.
            If not provided, a new session will be created.
        """
        async with self.database.must_enter_async_session(session) as session:
            await session.execute(self.table.delete())

    async def select(self, id: ID, *, session: AsyncSession | None = None) -> T | None:
        async with self.database.must_enter_async_session(session) as session:
            return await session.get(self.model, id)

    async def select_all(self, *, session: AsyncSession | None = None) -> Sequence[T]:
        stmt = select(self.model)
        async with self.database.must_enter_async_session(session) as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    @property
    def database(self) -> BaseMySQLDatabase:
        return self._database

    @property
    def model(self) -> type[T]:
        return self._model_cls

    @property
    def table(self) -> Table:
        return self.model.get_table()

    @property
    def table_name(self) -> str:
        return self.model.__tablename__

    def _get_primary_key(self) -> Tuple[Column[Any], ...] | Column[Any]:
        model_cls = self.model
        primary_keys: tuple[Column[Any], ...] | Column[Any] = model_cls.__mapper__.primary_key

        if not isinstance(primary_keys, tuple):  # type: ignore
            return tuple_(primary_keys)

        if len(primary_keys) == 1:
            return primary_keys[0]

        return tuple_(*primary_keys)

    @staticmethod
    def _ensure_iterable[U](obj: Iterable[U] | U) -> Iterable[U]:
        if isinstance(obj, Iterable):
            return obj
        else:
            return [obj]

    def _convert_comparable(self, id_: Iterable[ID] | ID) -> list[tuple[ID, ...]]:
        ids = self._ensure_iterable(id_)
        ret = [(id__,) for id__ in ids]
        return ret

    def _to_dict(self, objs: Iterable[T]) -> list[dict[str, Any]]:
        return [
            {c.name: getattr(obj, c.name) for c in obj.get_table().columns}
            for obj in objs
        ]
