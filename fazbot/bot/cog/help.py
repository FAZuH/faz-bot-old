from typing import Any

import nextcord

from ..invoked import Help as HelpCommand
from . import CogBase


class Help(CogBase):

    @nextcord.slash_command(name="help", description="Help command")
    async def _help(self, interaction: nextcord.Interaction[Any]) -> None:
        if not interaction.guild:
            await interaction.send("You can only use this command in a guild channel.")
            return
        cmds = [cmd for cmd in interaction.guild.get_application_commands()]
        await HelpCommand(interaction, cmds).run()
