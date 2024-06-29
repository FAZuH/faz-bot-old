from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, TYPE_CHECKING

from discord import Colour, Embed, Interaction
from nextcord.ext import commands

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fazbot import Bot, IFazBotDatabase, Logger


class CogBase(commands.Cog):

    __whitelisted_guild_ids: list[int] = []

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self._bot = bot

    def setup(self) -> None:
        """Adds cog to the bot."""
        self._bot.client.add_cog(self)
        self._setup()

        self._bot.logger.console.info(
            f"Added cog {self.__class__.__qualname__} to client "
            f"with {len(self.application_commands)} application commands"
        )
 
    @classmethod
    def get_whitelisted_guild_ids(cls) -> list[int]:
        return cls.__whitelisted_guild_ids

    @classmethod
    def set_whitelisted_guild_ids(cls, whitelisted_guild_ids: list[int]) -> None:
        cls.__whitelisted_guild_ids = whitelisted_guild_ids

    @property
    def logger(self) -> Logger:
        return self._bot.logger

    async def _respond_successful(self, interaction: Interaction[Any], message: str) -> None:
        embed = Embed(title="Success", description=message, color=Colour.dark_green())
        await interaction.response.send_message(embed=embed)

    async def _respond_error(self, interaction: Interaction[Any], message: str) -> None:
        embed = Embed(title="Error", description=message, color=Colour.dark_red())
        await interaction.response.send_message(embed=embed)

    @asynccontextmanager
    async def _enter_db_session(self) -> AsyncGenerator[tuple[IFazBotDatabase, AsyncSession], None]:
        with self._bot.core.enter_fazbotdb() as db:
            async with db.enter_session() as session:
                yield db, session

    def _setup(self) -> None:
        """Method to run on cog setup."""
        ...
