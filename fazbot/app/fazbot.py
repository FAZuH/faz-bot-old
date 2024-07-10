from __future__ import annotations
from contextlib import contextmanager
from threading import Lock
from typing import TYPE_CHECKING, Generator

from loguru import logger

from fazbot.bot import Bot
from fazbot.db.fazbot import FazbotDatabase
from fazbot.db.fazdb import FazdbDatabase

from ._logger import Logger
from .properties import Properties

if TYPE_CHECKING:
    from fazbot.db.fazbot import FazbotDatabase
    from fazbot.db.fazdb import FazdbDatabase


class App:

    def __init__(self) -> None:
        self._locks: dict[str, Lock] = {}

        self._properties = Properties()
        p = self.properties
        p.setup()
        Logger.setup(p.LOG_DIR, p.DISCORD_LOG_WEBHOOK, p.ADMIN_DISCORD_ID)

        self._fazbot_db = FazbotDatabase(
            "mysql+aiomysql",
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZBOT_DB_NAME
        )
        self._fazdb_db = FazdbDatabase(
            "mysql+aiomysql",
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZDB_DB_NAME
        )
        self._bot = Bot(self)

    def start(self) -> None:
        logger.info("Starting fazbot.app")
        self._bot.start()
        logger.success("Started fazbot.app", discord=True)

    def stop(self) -> None:
        logger.info("Stopping fazbot.app")
        self._bot.stop()
        logger.success("Stopped fazbot.app", discord=True)

    @property
    def properties(self) -> Properties:
        return self._properties

    @contextmanager
    def enter_bot(self) -> Generator[Bot]:
        with self._get_lock("bot"):
            yield self._bot

    @contextmanager
    def enter_fazbot_db(self) -> Generator[FazbotDatabase]:
        with self._get_lock("fazbotdb"):
            yield self._fazbot_db

    @contextmanager
    def enter_fazdb_db(self) -> Generator[FazdbDatabase]:
        with self._get_lock("fazdbdb"):
            yield self._fazdb_db

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
