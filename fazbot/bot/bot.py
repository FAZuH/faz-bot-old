from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from loguru import logger
from nextcord import Intents
from nextcord.ext import commands
from sqlalchemy.exc import IntegrityError

from ._asset_manager import AssetManager
from ._checks import Checks
from ._events import Events
from ._utils import Utils
from .cog.cog_core import CogCore

if TYPE_CHECKING:
    from fazbot.app import App


class Bot:

    def __init__(self, app: App) -> None:
        self._app = app

        self._fazbot_db = app.create_fazbot_db()
        self._fazdb_db = app.create_fazdb_db()

        # set intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        self._client = commands.Bot(intents=intents, help_command=None)
        
        self._event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._event_loop)
        self._discord_bot_thread = Thread(target=self._start, name=self._get_cls_qualname())

        # Define self._client before initializing the modules below
        self._asset_manager = AssetManager(self)
        self._checks = Checks(self)
        self._cogs = CogCore(self)
        self._events = Events(self)

        self.fazbot_db.create_all()
        self.fazdb_db.create_all()

    def start(self) -> None:
        logger.info(f"Starting Bot")
        self._discord_bot_thread.start()
        # Note: thread.start() runs self._start()
        logger.success(f"Started discord thread")

    def stop(self) -> None:
        logger.info(f"Stopping Bot")
        asyncio.run_coroutine_threadsafe(self._async_teardown(), self._event_loop).result()
        self._event_loop.stop()
        logger.success(f"Stopped Bot")

    async def _async_teardown(self) -> None:
        await self.client.close()
        await self.fazbot_db.teardown()
        await self.fazdb_db.teardown()

    async def on_ready_setup(self) -> None:
        """Setup after the bot is ready."""
        await self._whitelist_dev_guild()
        whitelisted_guild_ids = await self._get_whitelisted_guild_ids()
        await self.cogs.setup(whitelisted_guild_ids)
        await self._sync_dev_guild()

    @property
    def fazbot_db(self):
        return self._fazbot_db

    @property
    def fazdb_db(self):
        return self._fazdb_db

    @property
    def asset_manager(self) -> AssetManager:
        return self._asset_manager

    @property
    def cogs(self) -> CogCore:
        return self._cogs

    @property
    def app(self) -> App:
        return self._app

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
        logger.info(f"Starting discord client")
        asyncio.set_event_loop(self._event_loop)
        coro = self.client.start(self.app.properties.DISCORD_BOT_TOKEN)
        self._event_loop.create_task(coro)
        self._event_loop.run_forever()

    def _get_cls_qualname(self) -> str:
        return self.__class__.__qualname__

    async def _get_whitelisted_guild_ids(self) -> list[int]:
        db = self.fazbot_db
        guild_ids = await db.whitelist_group_repository.get_all_whitelisted_guild_ids()
        return list(guild_ids)

    async def _sync_dev_guild(self) -> None:
        """Synchronizes commands registered to dev guild into discord."""
        dev_server_id = self.app.properties.DEV_SERVER_ID
        await self.client.sync_application_commands(guild_id=dev_server_id)
        logger.info(f"Synchronized application commands for dev guild id {dev_server_id}")

    async def _whitelist_dev_guild(self) -> None:
        """Adds dev guild to whitelist database, if not already added."""
        guild = await Utils.must_get_guild(self.client, self.app.properties.DEV_SERVER_ID)
        try:
            await self.fazbot_db.whitelist_group_repository.whitelist_guild(
                guild.id,
                reason="DEV GUILD"
            )
        except IntegrityError:
            pass
