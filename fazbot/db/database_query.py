# pyright: reportUnknownVariableType=false, reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
from __future__ import annotations
from asyncio import Future
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator, Iterable, Mapping
from warnings import filterwarnings

from aiomysql import DictCursor, connect, Warning

from fazbot.util import ErrorHandler

if TYPE_CHECKING:
    from aiomysql import Connection

filterwarnings("ignore", category=Warning)


class DatabaseQuery:

    def __init__(self, user: str, password: str, database: str, retries: int = 0) -> None:
        self._user: str = user
        self._password: str = password
        self._database: str = database
        self._retries: int = retries
        self._retry_decorator = ErrorHandler.retry_decorator(self.retries, Exception)

    async def fetch(
        self,
        sql: str,
        params: None | tuple[Any, ...] | dict[str, Any] | Mapping[str, Any] = None,
        connection: None | Connection = None
    ) -> list[dict[str, Any]]:
        async with self.get_cursor(connection) as curs:
            await self._execute(curs, sql, params)
            conn: Connection = curs.connection  # type: ignore
            await conn.commit()
            return await curs.fetchall()

    async def fetch_many(
        self,
        sql: str,
        params: None | Iterable[tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]] = None,
        connection: None | Connection = None
    ) -> list[dict[str, Any]]:
        async with self.get_cursor(connection) as curs:
            await self._executemany(curs, sql, params)
            conn: Connection = curs.connection  # type: ignore
            await conn.commit()
            return await curs.fetchall()

    async def execute(
            self,
            sql: str,
            params: None | tuple[Any, ...] | dict[str, Any] | Mapping[str, Any] = None,
            connection: None | Connection = None
    ) -> int:
        async with self.get_cursor(connection) as curs:
            await self._execute(curs, sql, params)
            conn: Connection = curs.connection  # type: ignore
            await conn.commit()
            return curs.rowcount or 0

    async def execute_many(
        self,
        sql: str,
        params: None | Iterable[tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]] = None,
        connection: None | Connection = None
    ) -> int:
        async with self.get_cursor(connection) as curs:
            await self._executemany(curs, sql, params)
            conn: Connection = curs.connection  # type: ignore
            await conn.commit()
            return curs.rowcount or 0

    @asynccontextmanager
    async def get_cursor(self, conn: None | Connection = None) -> AsyncGenerator[DictCursor, Any]:
        if conn:
            async with conn.cursor(DictCursor) as curs:
                yield curs
        else:
            async with self.create_connection() as conn:
                async with conn.cursor(DictCursor) as curs:
                    yield curs

    @asynccontextmanager
    async def create_connection(self) -> AsyncGenerator[Connection, Any]:
        conn: Connection
        async with connect(user=self.user, password=self.password, db=self.database) as conn:
            yield conn

    def transaction_group(self) -> DatabaseQuery._TransactionGroupContextManager:
        return self._TransactionGroupContextManager(self)

    @property
    def user(self) -> str:
        return self._user

    @property
    def password(self) -> str:
        return self._password

    @property
    def database(self) -> str:
        return self._database

    @property
    def retries(self) -> int:
        return self._retries


    async def _execute(self, cursor: DictCursor, sql: str, params: None | tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]= None) -> None:
        decorated = self._retry_decorator(cursor.execute)
        await decorated(sql, params)

    async def _executemany(self, cursor: DictCursor, sql: str, params: None | Iterable[tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]] = None) -> None:
        decorated = self._retry_decorator(cursor.executemany)
        await decorated(sql, params)


    class _TransactionGroupContextManager:

        def __init__(self, parent: DatabaseQuery) -> None:
            self._parent: DatabaseQuery = parent
            self._sql: list[tuple[str, None | tuple[Any, ...] | dict[Any, Any]]] = []

            self._affectedrows: Future[int] = Future()

        async def __aenter__(self) -> DatabaseQuery._TransactionGroupContextManager:
            return self

        async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            async with self._parent.get_cursor() as curs:
                for q, p in self._sql:
                    if p:
                        await self._parent._executemany(curs, q, p)
                    else:
                        await self._parent._execute(curs, q)
                conn: Connection = curs.connection  # type: ignore
                await conn.commit()
                self._affectedrows.set_result(curs.rowcount or 0)

        def add(self, sql: str, params: None | tuple[Any, ...] | dict[Any, Any] = None) -> None:
            self._sql.append((sql, params))

        def get_future_affectedrows(self) -> Future[int]:
            return self._affectedrows
