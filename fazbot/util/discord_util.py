from typing import Any

from datetime import datetime
from dateparser import parse
from discord.ext import commands


class DiscordUtil:

    @staticmethod
    async def parse_big_int(ctx: commands.Context[Any], value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            await ctx.send(f"Failed parsing {value} into an integer.")

    @staticmethod
    async def parse_date(ctx: commands.Context[Any], value: str) -> datetime | None:
        try:
            return parse(value)
        except ValueError:
            await ctx.send(f"Failed parsing {value} into a date.")
