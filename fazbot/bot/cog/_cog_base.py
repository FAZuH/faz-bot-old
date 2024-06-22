from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Sequence, TYPE_CHECKING

from discord import Colour, Embed, Interaction
from nextcord.ext import commands

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fazbot import Bot, IFazBotDatabase


class CogBase(commands.Cog):

    __whitelisted_guild_ids: list[int] = []
    __initialized_whitelisted_guild_ids = False

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    @classmethod
    def get_whitelisted_guild_ids(cls) -> list[int]:
        return cls.__whitelisted_guild_ids

    @classmethod
    def set_whitelisted_guild_ids(cls, whitelisted_guild_ids: list[int]) -> None:
        cls.__initialized_whitelisted_guild_ids = True
        cls.__whitelisted_guild_ids = whitelisted_guild_ids

    def setup(self) -> None:
        self.__check_set_whitelisted_guild_ids()
        self._setup()

        guild_ids = self.get_whitelisted_guild_ids()
        self.__rollout_all_commands(guild_ids)
        self._bot.client.add_cog(self)

        with self._bot.core.enter_logger() as logger:
            logger.console.info(f"Added cog {self.__class__.__qualname__} to client.")

    @asynccontextmanager
    async def _enter_db_session(self) -> AsyncGenerator[tuple[IFazBotDatabase, AsyncSession], None]:
        with self._bot.core.enter_fazbotdb() as db:
            async with db.enter_session() as session:
                yield db, session

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
        """Method to run on cog initialization. Overriding this method is optional."""
        pass

    def __rollout_all_commands(self, guild_ids: Sequence[int]) -> None:
        for cmd in self.application_commands:
            for guild_id in guild_ids:
                cmd.add_guild_rollout(guild=guild_id)

    @classmethod
    def __check_set_whitelisted_guild_ids(cls) -> None:
        if not cls.__initialized_whitelisted_guild_ids:
            raise ValueError("whitelisted_guild_ids is not set. Set first with set_whitelisted_guild_ids()")
