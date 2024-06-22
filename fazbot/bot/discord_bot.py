from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from nextcord import Intents
from nextcord.ext import commands

from . import AssetManager, Bot, Checks, Events
from .cog import CogCore

if TYPE_CHECKING:
    from fazbot import Core


class DiscordBot(Bot):

    def __init__(self, core: Core) -> None:
        self._core = core

        self._asset_manager = AssetManager(self)
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
        with self.core.enter_logger() as logger:
            logger.console.info(f"Starting {self._get_cls_qualname()}...")

        self._discord_bot_thread.start()

        with self.core.enter_logger() as logger:
            logger.console.info(f"Started {self._get_cls_qualname()}.")

    def stop(self) -> None:
        with self.core.enter_logger() as logger:
            logger.console.info(f"Stopping {self._get_cls_qualname()}...")

        self._event_loop.run_until_complete(self.client.close())

    def setup(self) -> None:
        """Initial setup for the bot."""
        self.asset_manager.load_assets()
        whitelisted_guild_ids = self._event_loop.run_until_complete(
            self.get_whitelisted_guild_ids()
        )
        self.cogs.setup(whitelisted_guild_ids)
        self.checks.load_checks()
        self.events.load_events()

    @property
    def asset_manager(self) -> AssetManager:
        return self._asset_manager

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

    @property
    def events(self) -> Events:
        return self._events

    def _start(self) -> None:
        with self._core.enter_config() as config:
            bot_token = config.discord_bot_token

        self._event_loop.run_until_complete(self.client.start(bot_token))

    def _get_cls_qualname(self) -> str:
        return self.__class__.__qualname__

    async def get_whitelisted_guild_ids(self) -> list[int]:
        with self.core.enter_fazbotdb() as db:
            guild_ids = await db.whitelisted_guild_repository.get_all_whitelisted_guild_ids()
            return list(guild_ids)
