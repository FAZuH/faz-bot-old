from __future__ import annotations

import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from nextcord import Intents
from nextcord.ext import commands
from regex import D

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
        self._discord_bot_thread = Thread(target=self._start, daemon=True, name=self._get_cls_qualname())

    def start(self) -> None:
        self._core.logger.console_logger.info(f"Starting {self._get_cls_qualname()}...")
        self._setup()
        self._discord_bot_thread.start()
        self.core.logger.console_logger.info(f"Started {self._get_cls_qualname()}.")

    def stop(self) -> None:
        self.core.logger.console_logger.info(f"Stopping {self._get_cls_qualname()}...")
        self._event_loop.run_until_complete(self.client.close())

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
        self._event_loop.run_until_complete(self.client.start(self.core.config.secret.discord.bot_token))

    def _setup(self) -> None:
        """Initial setup for the bot."""
        self.cogs.load_assets()
        self._events.load_events()
        self.client.add_application_command_check(self.checks.is_not_banned)

    def _get_cls_qualname(self) -> str:
        return self.__class__.__qualname__
