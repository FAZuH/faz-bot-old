from __future__ import annotations
from typing import TYPE_CHECKING

from discord import app_commands

from ..app_command import HelpCommand
from . import CogBase

if TYPE_CHECKING:
    from discord import Interaction


class Help(CogBase):

    def _setup(self) -> None:
        self._commands.extend([
                self._help
        ])


    @app_commands.command(name="help", description="Help command")
    async def _help(self, interaction: Interaction) -> None:
        cmds = [
                cmd for cmd in self._bot.command_tree.get_commands(guild=interaction.guild)
                if isinstance(cmd, app_commands.Command)
        ]
        await HelpCommand(interaction, cmds).run()
