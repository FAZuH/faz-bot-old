from __future__ import annotations
from contextlib import contextmanager
from threading import Lock
from typing import Generator

from loguru import logger
from typing_extensions import deprecated

from fazbot.bot import Bot
from fazbot.db import FazbotDatabase, FazdbDatabase, MangaNotifyDatabase
from fazbot.heartbeat import Heartbeat

from ._logger_setup import LoggerSetup
from .properties import Properties


class App:

    def __init__(self) -> None:
        self._locks: dict[str, Lock] = {}

        self._properties = Properties()
        p = self.properties
        p.setup()
        LoggerSetup.setup(p.LOG_DIR, p.DISCORD_LOG_WEBHOOK, p.ADMIN_DISCORD_ID)

        self._fazbot_db = self.create_fazbot_db()
        self._fazdb_db = self.create_fazdb_db()
        self._manga_notify_db = self.create_manga_notify_db()
        self._bot = Bot(self)
        self._heartbeat = Heartbeat(self)

    def start(self) -> None:
        logger.info("Starting App")
        self._fazdb_db.create_all()
        self._fazbot_db.create_all()
        self._manga_notify_db.create_all()
        self._bot.start()
        self._heartbeat.start()
        logger.success("Started App", discord=True)

    def stop(self) -> None:
        logger.info("Stopping App")
        self._fazdb_db.engine.dispose()
        self._fazbot_db.engine.dispose()
        self._manga_notify_db.engine.dispose()
        self._bot.stop()
        self._heartbeat.stop()
        logger.success("Stopped App", discord=True)

    @property
    def properties(self) -> Properties:
        return self._properties

    @contextmanager
    def enter_bot(self) -> Generator[Bot]:
        with self._get_lock("bot"):
            yield self._bot

    @deprecated("Removed soon. replace with create db")
    @contextmanager
    def enter_fazbot_db(self) -> Generator[FazbotDatabase]:
        with self._get_lock("fazbot_db"):
            yield self._fazbot_db

    @deprecated("Removed soon. replace with create db")
    @contextmanager
    def enter_fazdb_db(self) -> Generator[FazdbDatabase]:
        with self._get_lock("fazdb_db"):
            yield self._fazdb_db

    @deprecated("Removed soon. replace with create db")
    @contextmanager
    def enter_manga_notify_db(self) -> Generator[MangaNotifyDatabase]:
        with self._get_lock("manga_notify_db"):
            yield self._manga_notify_db

    def create_fazbot_db(self) -> FazbotDatabase:
        p = self.properties
        return FazbotDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZBOT_DB_NAME
        )

    def create_fazdb_db(self) -> FazdbDatabase:
        p = self.properties
        return FazdbDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZDB_DB_NAME
        )

    def create_manga_notify_db(self) -> MangaNotifyDatabase:
        p = self.properties
        return MangaNotifyDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.MANGA_NOTIFY_DB_NAME
        )

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
