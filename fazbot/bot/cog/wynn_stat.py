from __future__ import annotations
from typing import Any

from discord.ext import commands

from . import CogBase


class WynnStat(CogBase):

    def setup(self) -> None:
        pass


    @commands.hybrid_command(name="worldlist")
    async def worldlist(self, ctx: commands.Context[Any], worlds: int = 10) -> None:
        return

    # @commands.hybrid_command(name="activity")
    # async def activity(self, ctx: commands.Context[Any], player: str | None = None, guild: str | None = None) -> None:
    #     return

    # @commands.hybrid_command(name="player")
    # async def player(self, ctx: commands.Context[Any]) -> None:
    #     return

    # @commands.hybrid_command(name="player_guilds")
    # async def player_guilds(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @commands.hybrid_command(name="guild")
    # async def guild(self, ctx: commands.Context[Any], guild: str) -> None:
    #     return

    # @commands.hybrid_command(name="guild_member")
    # async def guild_member(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @commands.hybrid_command(name="find_hunteds")
    # async def find_hunteds(self, ctx: commands.Context[Any], player: str) -> None:
    #     return

    # @commands.hybrid_command(name="find_returned")
    # async def find_returned(self, ctx: commands.Context[Any], player: str) -> None:
    #     return


# - worldlist
# - activity
# - player
# - player_guilds
# - guild
# - guild_member
# - find_hunteds
# - find_returned
