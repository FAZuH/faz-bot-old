from __future__ import annotations
from typing import TYPE_CHECKING


from .app import App
from fazbot import Config
from fazbot.bot import DiscordBot
from fazbot.heartbeat import SimpleHeartbeat
from fazbot.logger import FazBotLogger

if TYPE_CHECKING:
    from fazbot import Bot, Heartbeat, Logger


class FazBot(App):

    def __init__(self) -> None:
        self._config = Config()
        self._config.load_config()
        self._logger = FazBotLogger(self._config.logging.error_log_webhook, self._config.application.debug, self._config.application.admin_discord_id)
        self._heartbeat = SimpleHeartbeat(self)
        self._bot = DiscordBot(self)

    def start(self) -> None:
        self._logger.console_logger.info("Starting Heartbeat...")
        self.heartbeat.start()
        self._logger.console_logger.info("Starting DiscordBot...")
        self.bot.start()

    def stop(self) -> None:
        self._logger.console_logger.info("Stopping Heartbeat...")
        self.heartbeat.stop()
        self._logger.console_logger.info("Stopping DiscordBot...")
        self.bot.stop()

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
