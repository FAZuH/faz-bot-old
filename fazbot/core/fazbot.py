from __future__ import annotations
from contextlib import contextmanager
from threading import Lock
from typing import Generator, TYPE_CHECKING

from fazbot import Asset, Config
from fazbot.bot import DiscordBot
from fazbot.constants import Constants
from fazbot.db.fazbot import FazBotDatabase
from fazbot.heartbeat import SimpleHeartbeat
from fazbot.logger import FazBotLogger

from .core import Core

if TYPE_CHECKING:
    from fazbot import Bot, Heartbeat, Logger, IFazBotDatabase


class FazBot(Core):

    def __init__(self) -> None:
        self._locks: dict[str, Lock] = {}

        self._asset = Asset(Constants.ASSET_DIR)
        self._config = Config(Constants.CONFIG_FP)

        self._asset.read_all()
        self._config.read()

        with self.enter_config() as config:
            self._fazbotdb = FazBotDatabase(
                config.secret.fazbot.db_username,
                config.secret.fazbot.db_password,
                config.secret.fazbot.db_schema_name,
                config.secret.fazbot.db_max_retries,
            )
            self._logger = FazBotLogger(
                config.logging.discord_log_webhook,
                config.application.debug,
                config.application.admin_discord_id
            )

        self._heartbeat = SimpleHeartbeat(self)
        self._bot = DiscordBot(self)

    def start(self) -> None:
        self._heartbeat.start()
        self._bot.start()

    def stop(self) -> None:
        self._heartbeat.stop()
        self._bot.stop()

    @contextmanager
    def enter_asset(self) -> Generator[Asset]:
        with self._get_lock("asset"):
            yield self._asset

    @contextmanager
    def enter_bot(self) -> Generator[Bot]:
        with self._get_lock("bot"):
            yield self._bot

    @contextmanager
    def enter_config(self) -> Generator[Config]:
        with self._get_lock("config"):
            yield self._config

    @contextmanager
    def enter_fazbotdb(self) -> Generator[IFazBotDatabase]:
        with self._get_lock("fazbotdb"):
            yield self._fazbotdb

    @contextmanager
    def enter_heartbeat(self) -> Generator[Heartbeat]:
        with self._get_lock("heartbeat"):
            yield self._heartbeat

    @contextmanager
    def enter_logger(self) -> Generator[Logger]:
        with self._get_lock("logger"):
            yield self._logger

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock

