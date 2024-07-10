from typing import Any

import nextcord
from nextcord import Interaction, SlashOption

from ._cog_base import CogBase


class WynnStat(CogBase):

    @nextcord.slash_command(name="worldlist")
    async def worldlist(
            self,
            interaction: Interaction[Any],
            worlds: int = SlashOption(min_value=1, max_value=100, default=10)
        ) -> None:
        """Show list of worlds.

        Parameters
        ----------
        worlds : int
            Amount of worlds to show.
        """
        async with self._enter_fazdb_session() as (db, session):
            pass

    # @nextcord.slash_command(name="activity")
    # async def activity(self, interaction: Interaction[Any], player: str | None = None, guild: str | None = None) -> None:
    #     return

    # @nextcord.slash_command(name="player")
    # async def player(self, interaction: Interaction[Any]) -> None:
    #     return

    # @nextcord.slash_command(name="player_guilds")
    # async def player_guilds(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild")
    # async def guild(self, interaction: Interaction[Any], guild: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild_member")
    # async def guild_member(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_hunteds")
    # async def find_hunteds(self, interaction: Interaction[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_returned")
    # async def find_returned(self, interaction: Interaction[Any], player: str) -> None:
    #     return
