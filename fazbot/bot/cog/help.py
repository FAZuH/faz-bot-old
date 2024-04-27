from __future__ import annotations
from typing import TYPE_CHECKING, Any

from discord import app_commands

from ..invoked import Help as HelpCommand
from . import CogBase

if TYPE_CHECKING:
    from discord import Interaction


class Help(CogBase):

    @app_commands.command(name="help", description="Help command")
    async def _help(self, interaction: Interaction[Any]) -> None:
        cmds = [
                cmd for cmd in self._bot.bot.tree.get_commands(guild=interaction.guild)
                if isinstance(cmd, app_commands.Command)
        ]
        await HelpCommand(interaction, cmds).run()
