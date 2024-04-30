from __future__ import annotations

import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from nextcord import Intents
from nextcord.ext import commands

from . import Bot, Checks, CogCore, Events

if TYPE_CHECKING:
    from fazbot import Core


class DiscordBot(Bot):

    def __init__(self, core: Core) -> None:
        self._core = core

        self._checks = Checks(self)
        self._cogs = CogCore(self)
        self._events = Events(self)

        self._event_loop = asyncio.new_event_loop()

        # set intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self._client = commands.Bot('/', intents=intents, help_command=None)
        self._discord_bot_thread = Thread(target=self._start, daemon=True, name=self.__class__.__qualname__)

    def start(self) -> None:
        self._core.logger.console_logger.info(f"Starting {self.__class__.__qualname__}...")
        self._setup()
        self._discord_bot_thread.start()
        self._core.logger.console_logger.info(f"Started {self.__class__.__qualname__}.")

    def stop(self) -> None:
        self._core.logger.console_logger.info(f"Stopping {self.__class__.__qualname__}...")
        self._event_loop.run_until_complete(self._client.close())

    @property
    def cogs(self) -> CogCore:
        return self._cogs

    @property
    def core(self) -> Core:
        return self._core

    @property
    def client(self) -> commands.Bot:
        return self._client

    @property
    def checks(self) -> Checks:
        return self._checks

    def _start(self) -> None:
        self._event_loop.run_until_complete(self._client.start(self._core.config.secret.discord.bot_token))

    def _setup(self) -> None:
        """ Method to be run on start. """
        self._cogs.load_assets()
        self._client.add_check(self.checks.is_not_banned)
        self._events.load_events()
