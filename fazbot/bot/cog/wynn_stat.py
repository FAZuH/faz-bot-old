from typing import Any

import nextcord
from nextcord import Interaction

from . import CogBase


class WynnStat(CogBase):

    @nextcord.slash_command(name="worldlist")
    async def worldlist(self, interaction: Interaction[Any], worlds: int = 10) -> None:
        return

    # @nextcord.slash_command(name="activity")
    # async def activity(self, ctx: commands.Context[Any], player: str | None = None, guild: str | None = None) -> None:
    #     return

    # @nextcord.slash_command(name="player")
    # async def player(self, ctx: commands.Context[Any]) -> None:
    #     return

    # @nextcord.slash_command(name="player_guilds")
    # async def player_guilds(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild")
    # async def guild(self, ctx: commands.Context[Any], guild: str) -> None:
    #     return

    # @nextcord.slash_command(name="guild_member")
    # async def guild_member(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_hunteds")
    # async def find_hunteds(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @nextcord.slash_command(name="find_returned")
    # async def find_returned(self, ctx: commands.Context[Any], player: str) -> None:
    #     return
