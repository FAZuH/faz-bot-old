from __future__ import annotations

from typing import TYPE_CHECKING, Any

from nextcord import (Activity, ActivityType, ApplicationError, Interaction,
                      errors)
from nextcord.ext import commands
from nextcord.ext.commands import BucketType, Cooldown, CooldownMapping

if TYPE_CHECKING:
    from . import Bot

class Events:

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._cooldown = CooldownMapping(Cooldown(1, 3.), BucketType.user)
        self._ready = False

    def load_events(self) -> None:
        self._bot.client.add_listener(self.on_ready)
        self._bot.client.add_listener(self.on_command)
        self._bot.client.add_listener(self.on_command_error)
        self._bot.client.add_listener(self.on_command_completion)
        self._bot.client.add_listener(self.on_application_command_completion)
        self._bot.client.add_listener(self.on_application_command_error)
        self._bot.client.before_invoke(self.before_invoke)
        self._bot.client.application_command_before_invoke(self.before_application_invoke)

    async def on_ready(self) -> None:
        if self._bot.client.user is not None:
            await self._bot.core.logger.discord_logger.success(f"{self._bot.client.user.display_name} has successfully started.")

        await self._bot.client.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

        # on_ready can be called multiple times. don't setup cogs more than once
        if not self._ready:
            # Loads all cogs and commands to the client
            await self._bot.cogs.setup()
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

    async def on_application_command_completion(self, interaction: Interaction[Any]) -> None:
        self._log_event_to_console(interaction, self.on_application_command_completion.__name__)

    async def on_application_command_error(self, interaction: Interaction[Any], error: ApplicationError) -> None:
        self._log_event_to_console(interaction, self.on_application_command_error.__name__)
        if isinstance(error, errors.ApplicationCheckFailure):
            await interaction.send("You do not have permission to use this command.")
        else:
            await interaction.send(f"An error occurred while executing the command: {error}")

    async def before_invoke(self, ctx: commands.Context[Any]) -> None:
        self._log_event_to_console(ctx, self.before_invoke.__name__)
        self._ratelimit(ctx)

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
        self._bot.core.logger.console_logger.debug(message)
