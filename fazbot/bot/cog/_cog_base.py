from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Iterable, TYPE_CHECKING

from nextcord import Colour, Embed, Interaction
from nextcord.ext import commands

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fazbot import Bot, IFazbotDatabase, Logger, IFazdbDatabase


class CogBase(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self._bot = bot

    def setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Adds cog to the bot."""
        self._bot.client.add_cog(self)
        self._setup(whitelisted_guild_ids)

        self._bot.logger.console.info(
            f"Added cog {self.__class__.__qualname__} to client "
            f"with {len(self.application_commands)} application commands"
        )
 
    @property
    def logger(self) -> Logger:
        return self._bot.logger

    async def _respond_successful(self, interaction: Interaction[Any], message: str) -> None:
        embed = Embed(title="Success", description=message, color=Colour.dark_green())
        await interaction.send(embed=embed)

    @asynccontextmanager
    async def _enter_botdb_session(self) -> AsyncGenerator[tuple[IFazbotDatabase, AsyncSession], None]:
        with self._bot.core.enter_fazbotdb() as db:
            async with db.enter_session() as session:
                yield db, session

    @asynccontextmanager
    async def _enter_fazdb_session(self) -> AsyncGenerator[tuple[IFazdbDatabase, AsyncSession], None]:
        with self._bot.core.enter_fazdbdb() as db:
            async with db.enter_session() as session:
                yield db, session

    def _setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        """Method to run on cog setup.
        By default, this adds whitelisted_guild_ids into
        guild rollouts into all command in the cog."""
        for app_cmd in self.application_commands:
            for guild_id in whitelisted_guild_ids:
                app_cmd.add_guild_rollout(guild_id)
                # app_cmd.guild_ids.add(guild_id)
            self._bot.client.add_application_command(app_cmd, overwrite=True, use_rollout=True)
