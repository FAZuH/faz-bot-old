# pyright: reportUnknownVariableType=false, reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
from __future__ import annotations
from asyncio import Future
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Iterable, Mapping, TYPE_CHECKING
from warnings import filterwarnings

from aiomysql import DictCursor, MySQLError, Warning, connect

from fazbot.util import RetryHandler

if TYPE_CHECKING:
    from aiomysql import Connection

filterwarnings("ignore", category=Warning)


class DatabaseQuery:

    def __init__(self, host: str, user: str, password: str, database: str, retries: int = 0) -> None:
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._retries = retries

        self._retry_decorator = RetryHandler.decorator(self._retries, MySQLError)

    async def fetch(
        self,
        sql: str,
        params: None | tuple[Any, ...] | dict[str, Any] | Mapping[str, Any] = None,
        connection: None | Connection = None
    ) -> list[dict[str, Any]]:
        async with self.enter_cursor(connection) as curs:
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
        async with self.enter_cursor(connection) as curs:
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
        async with self.enter_cursor(connection) as curs:
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
        async with self.enter_cursor(connection) as curs:
            await self._executemany(curs, sql, params)
            conn: Connection = curs.connection  # type: ignore
            await conn.commit()
            return curs.rowcount or 0

    @asynccontextmanager
    async def enter_cursor(self, conn: None | Connection = None) -> AsyncGenerator[DictCursor, Any]:
        if conn:
            async with conn.cursor(DictCursor) as curs:
                yield curs
        else:
            async with self.enter_connection() as conn:
                async with conn.cursor(DictCursor) as curs:
                    yield curs

    @asynccontextmanager
    async def enter_connection(self) -> AsyncGenerator[Connection, Any]:
        conn: Connection
        async with connect(
            host=self._host,
            user=self._user,
            password=self._password,
            db=self._database
        ) as conn:
            yield conn

    def transaction_group(self) -> DatabaseQuery._TransactionGroupContextManager:
        return self._TransactionGroupContextManager(self)

    async def _execute(
            self,
            cursor: DictCursor,
            sql: str, params: None | tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]= None
        ) -> None:
        decorated = self._retry_decorator(cursor.execute)
        await decorated(sql, params)

    async def _executemany(
            self,
            cursor: DictCursor,
            sql: str,
            params: None | Iterable[tuple[Any, ...] | dict[str, Any] | Mapping[str, Any]] = None
        ) -> None:
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
            async with self._parent.enter_cursor() as curs:
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
