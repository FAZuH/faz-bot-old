from __future__ import annotations
import asyncio
from threading import Thread
from typing import TYPE_CHECKING, Any

from discord import Interaction
from nextcord import Activity, ActivityType, ApplicationError, errors, Guild, Intents
from nextcord.ext import commands

from . import Checks
from fazbot.enum import UserdataFile

from . import Bot, CogCore

if TYPE_CHECKING:
    from fazbot import Core


class DiscordBot(Bot):

    def __init__(self, app: Core) -> None:
        self._app = app

        self._checks = Checks(self._app)
        self._cooldown = commands.CooldownMapping(commands.Cooldown(1, 3.), commands.BucketType.user)
        self._event_loop = asyncio.new_event_loop()
        self._ready = False
        self._synced_guilds: list[Guild] = []

        # set intents
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self._bot = commands.Bot('/', intents=intents, help_command=None)
        self._cogs = CogCore(self, self._app)
        self._discord_bot_thread = Thread(target=self._start, daemon=True, name=self.__class__.__qualname__)

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
    def checks(self) -> Checks:
        return self._checks

    @property
    def synced_guilds(self) -> list[Guild]:
        return self._synced_guilds

    def _start(self) -> None:
        self._event_loop.run_until_complete(self._bot.start(self._app.config.secret.discord.bot_token))

    def _setup(self) -> None:
        """ Method to be run on start. """
        self._cogs.load_assets()
        self._bot.add_check(self.checks.is_not_banned)
        self._bot.add_listener(self.on_ready)
        self._bot.add_listener(self.on_command)
        self._bot.add_listener(self.on_command_error)
        self._bot.add_listener(self.on_command_completion)
        self._bot.add_listener(self.on_application_command_error)
        self._bot.add_listener(self.on_application_command_completion)
        self._bot.before_invoke(self.before_invoke)
        self._bot.application_command_before_invoke(self.before_application_invoke)

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

        if not self._ready:  # on_ready can be called multiple times. don't setup cogs more than once
            await self._cogs.setup(self._synced_guilds)  # Loads all cogs and commands to the client
        self._ready = True

    async def on_command(self, ctx: commands.Context[Any]) -> None:
        self._log_event_to_console(ctx, self.on_command.__name__)

    async def on_command_error(self, ctx: commands.Context[Any], error: commands.CommandError) -> None:
        self._log_event_to_console(ctx, self.on_command_error.__name__)
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            # TODO: log to admin
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after:.2f} seconds before using this command again.")
        else:
            await ctx.send(f"An error occurred while executing the command: {error}")

    async def on_command_completion(self, ctx: commands.Context[Any]) -> None:
        self._log_event_to_console(ctx, self.on_command_completion.__name__)
        # TODO: log to admin

    async def before_invoke(self, ctx: commands.Context[Any]) -> None:
        self._log_event_to_console(ctx, self.before_invoke.__name__)
        self._ratelimit(ctx)

    async def on_application_command_completion(self, interaction: Interaction[Any]) -> None:
        self._log_event_to_console(interaction, self.on_application_command_completion.__name__)

    async def on_application_command_error(self, interaction: Interaction[Any], error: ApplicationError) -> None:
        self._log_event_to_console(interaction, self.on_application_command_error.__name__)
        if isinstance(error, errors.ApplicationCheckFailure):
            await interaction.send("You do not have permission to use this command.")
        else:
            await interaction.send(f"An error occurred while executing the command: {error}")

    async def before_application_invoke(self, interaction: Interaction[Any]) -> None:
        self._log_event_to_console(interaction, self.before_application_invoke.__name__)
        self._ratelimit(interaction)

    def _ratelimit(self, ctx: commands.Context[Any] | Interaction[Any]) -> None:
        if not ctx.message:
            return
        bucket: commands.Cooldown = self._cooldown.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, self._cooldown.type)  # type: ignore

    def _log_event_to_console(self, ctx: commands.Context[Any] | Interaction[Any], event: str = '') -> None:
        if isinstance(ctx, commands.Context):
            if not ctx.command:
                return
            cmdname = ctx.command.name
            author = ctx.author.display_name
            guildname = ctx.guild.name if ctx.guild else None
            channelname = ctx.channel.name if ctx.channel and hasattr(ctx.channel, "name") else None  # type: ignore
            args = ctx.args, ctx.kwargs
        else:
            if not ctx.application_command:
                return
            cmdname = ctx.application_command.name
            author = ctx.user.display_name if ctx.user else None
            guildname = ctx.guild.name if ctx.guild else None
            channelname = ctx.channel.name if ctx.channel and hasattr(ctx.channel, "name") else None  # type: ignore
            data = ctx.data
            args = []
            if data:
                if "options" in data:
                    opts = data["options"]
                    for opt in opts:
                        if "options" in opt:
                            args.append(opt["options"])
        message = f"fired event {event}. name={cmdname}, author={author}"
        if guildname:
            message += f", guild={guildname}"
        if channelname:
            message += f", channel={channelname}"
        message += f", args={args}"
        self._app.logger.console_logger.debug(message)
