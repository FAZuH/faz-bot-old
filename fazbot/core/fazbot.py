from __future__ import annotations

from contextlib import contextmanager
from threading import Lock
from typing import TYPE_CHECKING, Generator

from fazbot import Config, ImageAsset, Userdata
from fazbot.bot import DiscordBot
from fazbot.heartbeat import SimpleHeartbeat
from fazbot.logger import FazBotLogger

from .core import Core

if TYPE_CHECKING:
    from fazbot import Bot, Heartbeat, Logger


class FazBot(Core):

    def __init__(self) -> None:
        self._config = Config()
        self._asset = ImageAsset()
        self._userdata = Userdata()
        self._locks: dict[str, Lock] = {}
        self._logger = FazBotLogger(
                self._config.logging.discord_log_webhook,
                self._config.application.debug,
                self._config.application.admin_discord_id
        )
        self._heartbeat = SimpleHeartbeat(self)
        self._bot = DiscordBot(self)

    def start(self) -> None:
        self.heartbeat.start()
        self.bot.start()

    def stop(self) -> None:
        self.heartbeat.stop()
        self.bot.stop()

    @property
    def bot(self) -> Bot:
        with self._get_lock("bot"):
            return self._bot

    @property
    def heartbeat(self) -> Heartbeat:
        with self._get_lock("heartbeat"):
            return self._heartbeat

    @contextmanager
    def get_asset_threadsafe(self) -> Generator[ImageAsset]:
        with self._get_lock("asset"):
            yield self._asset

    @contextmanager
    def get_config_threadsafe(self) -> Generator[Config]:
        with self._get_lock("config"):
            yield self._config

    @contextmanager
    def logger(self) -> Generator[Logger]:
        with self._get_lock("logger"):
            yield self._logger

    @contextmanager
    def userdata(self) -> Generator[Userdata]:
        with self._get_lock("userdata"):
            yield self._userdata

    def _setup(self) -> None:
        self._asset.load()
        self._config.load()
        self._userdata.load()

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
