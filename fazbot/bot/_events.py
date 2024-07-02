from __future__ import annotations
from datetime import datetime
import traceback
from typing import Any, TYPE_CHECKING

from nextcord import Activity, ActivityType, Colour, Embed, Interaction, errors
from nextcord.ext import commands
from nextcord.ext.commands import BucketType, Cooldown, CooldownMapping

from . import BotError, CommandFailure

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
            await self._bot.logger.discord.success(f"DiscordBot is ready!.")

        await self._bot.client.change_presence(activity=Activity(type=ActivityType.playing, name="/help"))

        # on_ready can be called multiple times. don't setup cogs more than once
        if not self._ready:
            # Loads all cogs and commands to the client
            await self._bot.on_ready_setup()

    async def on_application_command_completion(self, interaction: Interaction[Any]) -> None:
        await self.__log_event(interaction, self.on_application_command_completion.__name__)

    async def on_application_command_error(self, interaction: Interaction[Any], error: BaseException) -> None:
        await self.__log_event(interaction, self.on_application_command_error.__name__)

        if isinstance(error, errors.ApplicationCheckFailure):
            await interaction.send(
                ("You do not have permission to use this command. " 
                "Please contact bot developer if you believe this is a mistake."),
                ephemeral=True
            )
        elif isinstance(error, CommandFailure):
            await self.__send_expected_error(interaction, error)
        else:
            await self.__send_unexpected_error(interaction, error)

    async def before_application_invoke(self, interaction: Interaction[Any]) -> None:
        await self.__log_event(interaction, self.before_application_invoke.__name__)
        self.__ratelimit(interaction)

    def __ratelimit(self, interaction: Interaction[Any]) -> None:
        if not interaction.message:
            return

        bucket: commands.Cooldown = self._cooldown.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after, self._cooldown.type)  # type: ignore

    async def __log_event(self, interaction: Interaction[Any], event: str = '') -> None:
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

        self._bot.logger.console.info(message)
        await self._bot.logger.discord.info(message)

    async def __send_unexpected_error(self, interaction: Interaction[Any], exception: BaseException) -> None:
        embed_description = f"An unexpected error occurred while executing the command: \n**{exception}**"
        embed = Embed(title="Error", description=embed_description, color=Colour.red())
        embed.add_field(name="Timestamp", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=False)

        is_admin = await self._bot.checks.is_admin(interaction)
        if is_admin:
            tb = traceback.format_exception(exception)
            tb_msg = f"{'\n'.join(tb)}"[:1016]
            tb_msg = f"```{tb_msg}```"
            embed.add_field(name='Traceback', value=tb_msg, inline=False)

        await self._bot.logger.discord.error(exception=exception)
        await interaction.send(embed=embed, ephemeral=is_admin)

    async def __send_expected_error(self, interaction: Interaction[Any], exception: BotError) -> None:
        embed_description = f"An error occurred while executing the command: \n**{exception}**"
        embed = Embed(title="Error", description=embed_description, color=Colour.red())
        embed.add_field(name="Timestamp", value=f"<t:{int(datetime.now().timestamp())}:F>", inline=False)
        await interaction.send(embed=embed)
