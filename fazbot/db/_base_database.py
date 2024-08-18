from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Generator, TYPE_CHECKING

from sqlalchemy import Connection, URL, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession
    from . import BaseRepository, BaseModel


class BaseDatabase(ABC):
    """Abstract base class for database operations, supporting both synchronous and asynchronous drivers."""

    def __init__(
            self,
            sync_driver: str,
            async_driver: str,
            user: str,
            password: str,
            host: str,
            port: int,
            database: str,
        ) -> None:
        """Initialize the database with connection parameters.

        Args:
            sync_driver (str): Synchronous database driver.
            async_driver (str): Asynchronous database driver.
            user (str): Database user.
            password (str): Database password.
            host (str): Database host.
            port (int): Database port.
            database (str): Database name.
        """
        self._sync_driver = sync_driver
        self._async_driver = async_driver
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

        async_url = URL.create(async_driver, user, password, host, port, database)
        url = URL.create(sync_driver, user, password, host, port, database)
        self._async_engine = create_async_engine(async_url)
        self._engine = create_engine(url)

        self._repositories: list[BaseRepository[Any, Any]] = []

    def create_all(self) -> None:
        """Create all tables in the database."""
        self.base_model.metadata.create_all(bind=self.engine, checkfirst=True)

    def drop_all(self) -> None:
        """Drop all tables in the database."""
        self.base_model.metadata.drop_all(bind=self.engine, checkfirst=True)

    async def teardown(self) -> None:
        """Dispose database resources. This object cannot be used for database operations after this."""
        await self.async_engine.dispose()
        self.engine.dispose()

    @contextmanager
    def enter_connection(self) -> Generator[Connection, None]:
        """Provide a context manager for synchronous database connections.

        Yields:
            Generator[Connection, None]: Synchronous database connection.
        """
        with self.engine.begin() as conn:
            yield conn

    @contextmanager
    def enter_session(self) -> Generator[Session, None]:
        """Provide a context manager for synchronous database sessions.

        Yields:
            Generator[Session, None]: Synchronous database session.
        """
        with self.enter_connection() as conn:
            session = sessionmaker(bind=conn, autoflush=False, expire_on_commit=False)
            with session.begin() as session:
                yield session

    @contextmanager
    def must_enter_connection(self, connection: Connection | None = None) -> Generator[Connection, None]:
        """Provide a context manager for synchronous database connections, optionally reusing an existing connection.

        Args:
            connection (Connection | None): Existing synchronous database connection.

        Yields:
            Generator[Connection, None]: Synchronous database connection.
        """
        if connection:
            yield connection
        else:
            with self.enter_connection() as connection:
                yield connection

    @contextmanager
    def must_enter_session(self, session: Session | None = None) -> Generator[Session, None]:
        """Provide a context manager for synchronous database sessions, optionally reusing an existing session.

        Args:
            session (Session | None): Existing synchronous database session.

        Yields:
            Generator[Session, None]: Synchronous database session.
        """
        if session:
            yield session
        else:
            with self.enter_session() as session:
                yield session

    @asynccontextmanager
    async def enter_async_connection(self) -> AsyncGenerator[AsyncConnection, None]:
        """Provide a context manager for asynchronous database connections.

        Yields:
            AsyncGenerator[AsyncConnection, None]: Asynchronous database connection.
        """
        async with self.async_engine.begin() as conn:
            yield conn

    @asynccontextmanager
    async def enter_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide a context manager for asynchronous database sessions.

        Yields:
            AsyncGenerator[AsyncSession, None]: Asynchronous database session.
        """
        async with self.enter_async_connection() as conn:
            async_session = async_sessionmaker(bind=conn, autoflush=False, expire_on_commit=False)
            async with async_session.begin() as session:
                yield session

    @asynccontextmanager
    async def must_enter_async_connection(self, connection: AsyncConnection | None = None) -> AsyncGenerator[AsyncConnection, None]:
        """Provide a context manager for asynchronous database connections, optionally reusing an existing connection.

        Args:
            connection (AsyncConnection | None): Existing asynchronous database connection.

        Yields:
            AsyncGenerator[AsyncConnection, None]: Asynchronous database connection.
        """
        if connection:
            yield connection
        else:
            async with self.enter_async_connection() as connection:
                yield connection

    @asynccontextmanager
    async def must_enter_async_session(self, session: AsyncSession | None = None) -> AsyncGenerator[AsyncSession, None]:
        """Provide a context manager for asynchronous database sessions, optionally reusing an existing session.

        Args:
            session (AsyncSession | None): Existing asynchronous database session.

        Yields:
            AsyncGenerator[AsyncSession, None]: Asynchronous database session.
        """
        if session:
            yield session
        else:
            async with self.enter_async_session() as session:
                yield session

    @property
    def async_engine(self) -> AsyncEngine:
        """Get the asynchronous SQLAlchemy engine.

        Returns:
            AsyncEngine: Asynchronous SQLAlchemy engine.
        """
        return self._async_engine

    @property
    def engine(self) -> Engine:
        """Get the synchronous SQLAlchemy engine.

        Returns:
            Engine: Synchronous SQLAlchemy engine.
        """
        return self._engine

    @property
    def repositories(self) -> list[BaseRepository[Any, Any]]:
        """Get the list of repositories associated with the database.

        Returns:
            list[BaseRepository[Any, Any]]: List of repositories.
        """
        return self._repositories

    @property
    @abstractmethod
    def base_model(self) -> BaseModel:
        """Get the base model for the database."""
        pass
