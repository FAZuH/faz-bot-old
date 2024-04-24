# pyright: strict
from __future__ import annotations
from typing import TYPE_CHECKING

from discord.app_commands import Group, command, describe

from . import GroupBase

if TYPE_CHECKING:
    from discord import Interaction


class Admin(GroupBase, Group):

    def setup(self) -> None:
        Group.__init__(self, name="admin", description="Admin command group.")
        self._setup(self)

    @command(name="echo", description="Echoes a message.", )
    @describe(message="Message to echo.")
    async def _echo(self, interaction: Interaction, message: str) -> None:
        await interaction.response.send_message(message)

    @command(name="reload_config", description="Reloads configs.")
    async def _reload_config(self, interaction: Interaction) -> None:
        self._app.config.load_config()
        await interaction.response.send_message("Reloaded config successfully.")

    @command(name="sync", description="Resynchronizes commands with Discord.")
    async def _sync(self, interaction: Interaction) -> None:
        cmds = await self._bot.command_tree.sync()
        await interaction.response.send_message(f"Synchronized {len(cmds)} commands.")

    @command(name="shutdown", description="Shuts down the bot.")
    async def _shutdown(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Shutting down...")
        self._bot.stop()

    # @command(name="restart_bot", description="Restarts the bot.")
    # async def _restart_bot(self, interaction: Interaction) -> None:
    #     await interaction.response.send_message("Restarting bot...")
    #     await self._bot.restart()
