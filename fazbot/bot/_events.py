from __future__ import annotations

import traceback
from datetime import datetime
from typing import TYPE_CHECKING, Any

from nextcord import (Activity, ActivityType, ApplicationError, Colour, Embed, Interaction, errors)
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
        """Loads events to the client."""
        self._bot.client.add_listener(self.on_ready)
        self._bot.client.add_listener(self.on_application_command_completion)
        self._bot.client.add_listener(self.on_application_command_error)
        self._bot.client.application_command_before_invoke(self.before_application_invoke)

    async def on_ready(self) -> None:
        if self._bot.client.user is not None:
            with self._bot.core.enter_logger() as logger:
                await logger.discord.success(f"{self._bot.client.user.display_name} has successfully started.")

        await self._bot.client.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

        # on_ready can be called multiple times. don't setup cogs more than once
        if not self._ready:
            # Loads all cogs and commands to the client
            self._bot.setup()
        self._ready = True

    async def on_application_command_completion(self, interaction: Interaction[Any]) -> None:
        self._log_event_to_console(interaction, self.on_application_command_completion.__name__)

    async def on_application_command_error(self, interaction: Interaction[Any], error: ApplicationError) -> None:
        self._log_event_to_console(interaction, self.on_application_command_error.__name__)
        is_admin = self._bot.checks.is_admin(interaction)
        if isinstance(error, errors.ApplicationCheckFailure):
            await interaction.send("You do not have permission to use this command.", ephemeral=True)
        else:
            embed = self._get_unexpected_error_embed(error, is_admin)
            await interaction.send(embed=embed, ephemeral=True)

    async def before_application_invoke(self, interaction: Interaction[Any]) -> None:
        self._log_event_to_console(interaction, self.before_application_invoke.__name__)
        self._ratelimit(interaction)

    def _ratelimit(self, interaction: Interaction[Any]) -> None:
        if not interaction.message:
            return
        bucket: commands.Cooldown = self._cooldown.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, self._cooldown.type)  # type: ignore

    def _log_event_to_console(self, interaction: Interaction[Any], event: str = '') -> None:
        if not interaction.application_command:
            return

        cmdname = interaction.application_command.name
        author = interaction.user.display_name if interaction.user else None
        guildname = interaction.guild.name if interaction.guild else None
        channelname = interaction.channel.name if interaction.channel and hasattr(interaction.channel, "name") else None  # type: ignore
        data = interaction.data

        args = []
        if data and "options" in data:
            for opt in data["options"]:
                if "options" in opt:
                    args.append(opt["options"])
        message = f"fired event {event}. name={cmdname}, author={author}"
        if guildname:
            message += f", guild={guildname}"
        if channelname:
            message += f", channel={channelname}"
        message += f", args={args}"

        with self._bot.core.enter_logger() as logger:
            logger.console.debug(message)

    def _get_unexpected_error_embed(self, exception: BaseException, is_traceback: bool) -> Embed:
        embed_description = f"An error occurred while executing the command: {exception}"
        embed = Embed(title="Error", description=embed_description, color=Colour.red())
        if is_traceback:
            tb = traceback.format_exception(exception)
            embed.add_field(name=f"`{exception}`", value=f"```{''.join(tb)}```")
        embed.set_footer(text=f"<t:{int(datetime.now().timestamp())}:F>")
        return embed

    # TODO: Implement this
    # def _get_handled_error_embed(self, exception: BaseException, is_traceback: bool) -> Embed:
        # embed_description = f"An error occurred while executing the command: {exception}"
        # embed = Embed(title="Error", description=embed_description, color=Colour.red())
        # if is_traceback:
        #     tb = traceback.format_exception(exception)
        #     embed.add_field(name=f"`{exception}`", value=f"```{''.join(tb)}```")
        # embed.set_footer(text=f"<t:{int(datetime.now().timestamp())}:F>")
        # return embed
