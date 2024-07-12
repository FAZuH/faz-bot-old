from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, TYPE_CHECKING, Generator

from sqlalchemy import URL, Connection, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession
    from . import BaseRepository, BaseModel


class BaseMySQLDatabase(ABC):

    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            port: int,
            database: str,
        ) -> None:
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

        async_url = URL.create("mysql+aiomysql", user, password, host, port, database)
        url = URL.create("mysql+pymysql", user, password, host, port, database)
        self._async_engine = create_async_engine(async_url)
        self._engine = create_engine(url)

        self._repositories: list[BaseRepository[Any, Any]] = []

    def create_all(self) -> None:
        self.base_model.metadata.create_all(bind=self.engine, checkfirst=True)

    def drop_all(self) -> None:
        self.base_model.metadata.drop_all(bind=self.engine, checkfirst=True)

    @contextmanager
    def enter_connection(self) -> Generator[Connection, None]:
        with self.engine.begin() as conn:
            yield conn

    @contextmanager
    def enter_session(self) -> Generator[Session, None]:
        session = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        with session.begin() as session:
            yield session

    @contextmanager
    def must_enter_connection(self, connection: Connection | None = None) -> Generator[Connection, None]:
        if connection:
            yield connection
        else:
            with self.enter_connection() as connection:
                yield connection

    @contextmanager
    def must_enter_session(self, session: Session | None = None) -> Generator[Session, None]:
        if session:
            yield session
        else:
            with self.enter_session() as session:
                yield session

    @asynccontextmanager
    async def enter_async_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.async_engine.begin() as conn:
            yield conn

    @asynccontextmanager
    async def enter_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async_session = async_sessionmaker(bind=self.async_engine, autoflush=False, expire_on_commit=False)
        async with async_session.begin() as session:
            yield session

    @asynccontextmanager
    async def must_enter_async_connection(self, connection: AsyncConnection | None = None) -> AsyncGenerator[AsyncConnection, None]:
        if connection:
            yield connection
        else:
            async with self.enter_async_connection() as connection:
                yield connection

    @asynccontextmanager
    async def must_enter_async_session(self, session: AsyncSession | None = None) -> AsyncGenerator[AsyncSession, None]:
        if session:
            yield session
        else:
            async with self.enter_async_session() as session:
                yield session

    @property
    def async_engine(self) -> AsyncEngine:
        return self._async_engine

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def repositories(self) -> list[BaseRepository[Any, Any]]:
        return self._repositories

    @property
    @abstractmethod
    def base_model(self) -> BaseModel: ...
