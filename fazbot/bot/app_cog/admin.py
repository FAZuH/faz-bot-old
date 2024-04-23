from __future__ import annotations
from typing import TYPE_CHECKING

from discord import app_commands

from . import CogBase

if TYPE_CHECKING:
    from discord import Interaction


class Admin(CogBase):

    def _setup(self) -> None:
        self._commands.extend([
                self._echo,
                self._reload_config,
                self._sync
        ])

    @app_commands.command(description="Echoes a message back.")
    @app_commands.describe(message="Message to echo.")
    async def _echo(self, interaction: Interaction, message: str) -> None:
        await interaction.response.send_message(message)

    @app_commands.command(description="Reloads application configs.")
    async def _reload_config(self, interaction: Interaction) -> None:
        self._app.config.load_config()
        await interaction.response.send_message("Reloaded config successfully.")

    @app_commands.command(description="Resynchronizes commands with Discord.")
    async def _sync(self, interaction: Interaction) -> None:
        cmds = await self._bot.command_tree.sync()
        await interaction.response.send_message(f"Resynchronized {len(cmds)} commands.")
