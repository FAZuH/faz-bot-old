from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from discord import Colour, Embed, Interaction
from nextcord import ClientException
from nextcord.ext import commands

if TYPE_CHECKING:
    from fazbot import Bot


class CogBase(commands.Cog):

    _whitelisted_guild_ids: set[int] = set()

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self.setup()

    def setup(self) -> None:
        self._setup()

        with self._bot.core.enter_fazbotdb() as db:
            eventloop = asyncio.get_event_loop()
            guild_ids = eventloop.run_until_complete(db.whitelisted_guild_repository.get_all_whitelisted_guild_ids())

        for cmd in self.application_commands:
            for guild_id in guild_ids:
                assert isinstance(guild_id, int)
                cmd.add_guild_rollout(guild=guild_id)

        try:
            self._bot.client.add_cog(self)

            with self._bot.core.enter_logger() as logger:
                logger.console.info(f"Added cog {self.__class__.__qualname__} to client.")
        except ClientException:
            # this usually only happens on tests
            pass

    async def _respond_successful(self, interaction: Interaction[Any], message: str) -> None:
        embed = Embed(
            title="Success",
            description=message,
            color=Colour.dark_green()
        )
        await interaction.response.send_message(embed=embed)

    async def _respond_error(self, interaction: Interaction[Any], message: str) -> None:
        embed = Embed(
            title="Error",
            description=message,
            color=Colour.dark_red()
        )
        await interaction.response.send_message(embed=embed)

    def _setup(self) -> None:
        """Method to be run on cog initialization. Override this method in subclasses."""
        pass

