from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING

from discord import Activity, ActivityType, Client, Intents
from discord.app_commands import CommandTree

from . import Bot, Cogs

if TYPE_CHECKING:
    from fazbot import App


class DiscordBot(Bot):

    def __init__(self, app: App) -> None:
        self._app = app
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self._client = Client(intents=intents)
        self._command_tree = CommandTree(self.client)
        self._cogs = Cogs(self, self._app)

        self._discord_bot_thread = Thread(target=self._client.run, args=(self._app.config.secret.discord.bot_token,), daemon=True)
        self._event_loop = asyncio.new_event_loop()

    def start(self) -> None:
        self._setup()
        self._discord_bot_thread.start()

    def stop(self) -> None:
        self._event_loop.run_until_complete(self._client.close())

    @property
    def client(self) -> Client:
        return self._client

    @property
    def command_tree(self) -> CommandTree:
        return self._command_tree

    # @property
    # def registered_guilds(self) -> list[Guild]:
    #     return self._registered_guilds


    def _setup(self) -> None:
        """ Method to be run on discord bot thread. """
        @self.client.event
        async def on_ready() -> None:  # type: ignore
            if self.client.user is not None:
                # TODO: success webhook
                await self._app.logger.discord_logger.success(f"{self.client.user.display_name} has successfully started.")

            await self.client.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

            # TODO: create appdata folder for stuffs like these
            # # Fetch guilds before Cogs.setup()
            # guilds: list[Guild] = []
            # for id_ in self._app.registered_guild_ids:
            #     guild = self.client.get_guild(id_)
            #     if guild is not None:
            #         guilds.append(guild)

            # self._cogs.setup(guilds)  # Loads all cogs and commands

            # # Synchronizes commands
            # for guild in guilds:
            #     self._app.logger.console_logger.debug(f"Synchronizing commands for guild {guild.name} ({guild.id}).")
            #     cmds = await self._command_tree.sync(guild=guild)
            #     self._app.logger.console_logger.success(f"Synchronized {len(cmds)} commands in {guild.name} ({guild.id}).")
