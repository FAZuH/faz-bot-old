from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING

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
        self.config.load()
        self.asset.load()
        self.userdata.load()
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
    def asset(self) -> ImageAsset:
        with self._get_lock("asset"):
            return self._asset

    @property
    def bot(self) -> Bot:
        with self._get_lock("asset"):
            return self._bot

    @property
    def config(self) -> Config:
        with self._get_lock("asset"):
            return self._config

    @property
    def heartbeat(self) -> Heartbeat:
        with self._get_lock("asset"):
            return self._heartbeat

    @property
    def logger(self) -> Logger:
        with self._get_lock("asset"):
            return self._logger

    @property
    def userdata(self) -> Userdata:
        with self._get_lock("asset"):
            return self._userdata

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
