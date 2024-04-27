from __future__ import annotations
from typing import TYPE_CHECKING

from .core import Core
from fazbot import ImageAsset, Config, Userdata
from fazbot.bot import DiscordBot
from fazbot.heartbeat import SimpleHeartbeat
from fazbot.logger import FazBotLogger

if TYPE_CHECKING:
    from fazbot import Bot, Heartbeat, Logger


class FazBot(Core):

    def __init__(self) -> None:
        self._config = Config()
        self._config.load()
        self._asset = ImageAsset()
        self._userdata = Userdata()
        self._logger = FazBotLogger(
                self._config.logging.error_log_webhook,
                self._config.application.debug,
                self._config.application.admin_discord_id
        )
        self._heartbeat = SimpleHeartbeat(self)
        self._bot = DiscordBot(self)

    def start(self) -> None:
        self._asset.load()
        self._userdata.load()
        self.heartbeat.start()
        self.bot.start()

    def stop(self) -> None:
        self.heartbeat.stop()
        self.bot.stop()

    @property
    def asset(self) -> ImageAsset:
        return self._asset

    @property
    def bot(self) -> Bot:
        return self._bot

    @property
    def config(self) -> Config:
        return self._config

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def userdata(self) -> Userdata:
        return self._userdata
