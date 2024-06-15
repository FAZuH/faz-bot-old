from __future__ import annotations
from contextlib import asynccontextmanager
from typing import AsyncGenerator, TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession


class BaseDatabase:

    def __init__(
            self,
            driver: str,
            user: str,
            password: str,
            host: str,
            database: str,
        ) -> None:
        db_url = f"{driver}://{user}:{password}@{host}/{database}?charset=utf8mb4"
        self._engine = create_async_engine(db_url)

    @asynccontextmanager
    async def enter_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.connect() as conn:
            yield conn

    @asynccontextmanager
    async def enter_session(self) -> AsyncGenerator[AsyncSession, None]:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session.begin() as session:
            yield session

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

