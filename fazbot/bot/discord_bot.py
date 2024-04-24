# pyright: reportMissingTypeStubs=false
from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from discord import Activity, ActivityType, Guild, Intents
from discord.ext.commands import Bot as Bot_

from . import Bot, CogCore

if TYPE_CHECKING:
    from fazbot import App


class DiscordBot(Bot):

    def __init__(self, app: App) -> None:
        self._app = app
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self._bot = Bot_('/', intents=intents, help_command=None)
        self._cogs = CogCore(self, self._app)
        self._synced_guilds: list[Guild] = []

        self._discord_bot_thread = Thread(target=self._bot.run, args=(self._app.config.secret.discord.bot_token,), daemon=True)
        self._event_loop = asyncio.new_event_loop()

    def start(self) -> None:
        self._setup()
        self._discord_bot_thread.start()

    def stop(self) -> None:
        self._event_loop.run_until_complete(self._bot.close())

    @property
    def bot(self) -> Bot_:
        return self._bot

    @property
    def synced_guilds(self) -> list[Guild]:
        return self._synced_guilds


    def _setup(self) -> None:
        """ Method to be run on discord bot thread. """
        @self.bot.event
        async def on_ready() -> None:  # type: ignore
            if self.bot.user is not None:
                # TODO: success webhook
                await self._app.logger.discord_logger.success(f"{self.bot.user.display_name} has successfully started.")

            await self.bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

            # Fetch guilds before Cogs.setup()
            for id_ in self._app.config.authorized_guilds:
                guild = self.bot.get_guild(id_)
                if guild:
                    self._synced_guilds.append(guild)

            await self._cogs.setup(self._synced_guilds)  # Loads all cogs and commands to the client
