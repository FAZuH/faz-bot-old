# pyright: reportMissingTypeStubs=false
from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING, Any

from discord import Activity, ActivityType, ChannelType, errors, Guild, Intents
from discord.ext import commands

from fazbot.enum import UserdataFile
from fazbot.util import DiscordChecks

from . import Bot, CogCore

if TYPE_CHECKING:
    from fazbot import Core


class DiscordBot(Bot):

    def __init__(self, app: Core) -> None:
        self._app = app

        self._checks = DiscordChecks(self._app)
        self._synced_guilds: list[Guild] = []
        self._event_loop = asyncio.new_event_loop()

        # set intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self._bot = commands.Bot('/', intents=intents, help_command=None)
        self._cogs = CogCore(self, self._app)
        self._discord_bot_thread = Thread(target=self._bot.run, args=(self._app.config.secret.discord.bot_token,), daemon=True)

    def start(self) -> None:
        self._app.logger.console_logger.info(f"Starting {self.__class__.__qualname__}...")
        self._setup()
        self._discord_bot_thread.start()
        self._app.logger.console_logger.info(f"Started {self.__class__.__qualname__}.")

    def stop(self) -> None:
        self._app.logger.console_logger.info(f"Stopping {self.__class__.__qualname__}...")
        self._event_loop.run_until_complete(self._bot.close())

    @property
    def bot(self) -> commands.Bot:
        return self._bot

    @property
    def checks(self) -> DiscordChecks:
        return self._checks

    @property
    def synced_guilds(self) -> list[Guild]:
        return self._synced_guilds


    def _setup(self) -> None:
        """ Method to be run on start. """
        self._cogs.load_assets()
        self._bot.add_check(self._checks.is_not_banned)
        self._bot.add_listener(self.on_ready)
        self._bot.add_listener(self.on_command_error)
        self._bot.add_listener(self.on_command_completion)

    async def on_ready(self) -> None:
        if self.bot.user is not None:
            await self._app.logger.discord_logger.success(f"{self.bot.user.display_name} has successfully started.")

        await self.bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

        # Fetch guilds before Cogs.setup()
        for id_ in self._app.userdata.get(UserdataFile.WHITELISTED_GUILDS):  # type: ignore
            id_: int
            guild = self.bot.get_guild(id_)
            try:
                if not guild:
                    guild = await self.bot.fetch_guild(id_)
            except errors.Forbidden as e:
                await self._app.logger.discord_logger.exception(f"An error occurred while fetching guild with ID: {id_}: {e}")
                continue
            except errors.HTTPException as e:
                await self._app.logger.discord_logger.exception(f"An HTTP exception occurred while fetching guild with ID: {id_}: {e}")
                continue
            self._synced_guilds.append(guild)

        await self._cogs.setup(self._synced_guilds)  # Loads all cogs and commands to the client

    async def on_command_error(self, ctx: commands.Context[Any], error: commands.CommandError) -> None:
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            # TODO: log to admin
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        # command error response should be handled by the command itself, not here

    async def on_command_completion(self, ctx: commands.Context[Any]) -> None:
        # TODO: log to admin
        if not ctx.command:
            return
        message = f"fired event on_command_completion name={ctx.command.name}, author={ctx.author.display_name}"
        if ctx.guild and ctx.channel and ctx.channel.type != ChannelType.private:
            message += f", guild={ctx.guild.name}, channel={ctx.channel.name}"  # type: ignore
        message += f", args={ctx.args}, kwargs={ctx.kwargs}"
        self._app.logger.console_logger.debug(message)
