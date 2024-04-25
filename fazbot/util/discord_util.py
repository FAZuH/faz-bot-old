from typing import Any
from discord.ext import commands


class DiscordUtil:

    _admin_discord_id = -1

    @staticmethod
    def is_admin(ctx: commands.Context[Any]) -> bool:
        return ctx.author.id == DiscordUtil.get_admin_discord_id()

    @classmethod
    def get_admin_discord_id(cls) -> int:
        return cls._admin_discord_id

    @classmethod
    def set_admin_discord_id(cls, discord_id: int) -> None:
        cls._admin_discord_id = discord_id

    @staticmethod
    async def parse_big_int(ctx: commands.Context[Any], value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            await ctx.send(f"Failed parsing {value} into an integer.")
