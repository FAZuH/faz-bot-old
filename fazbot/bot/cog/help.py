from typing import Any

import nextcord

from ..errors import ApplicationException
from ..invoke import InvokeHelp as InvokeHelp
from ._cog_base import CogBase


class Help(CogBase):

    @nextcord.slash_command(name="help", description="Help command")
    async def _help(self, interaction: nextcord.Interaction[Any]) -> None:
        if not interaction.guild:
            raise ApplicationException("You can only use this command in a guild channel.")

        cmds = [cmd for cmd in interaction.guild.get_application_commands()]
        await InvokeHelp(self._bot, interaction, cmds).run()
