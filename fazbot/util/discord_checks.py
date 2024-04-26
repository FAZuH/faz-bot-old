from __future__ import annotations
from typing import TYPE_CHECKING, Any
from discord.ext import commands

from fazbot.enum import UserdataFile

if TYPE_CHECKING:
    from fazbot import Core


class DiscordChecks:

    def __init__(self, app: Core) -> None:
        self._app = app

    async def is_admin(self, ctx: commands.Context[Any]) -> bool:
        is_admin = ctx.author.id == self._app.config.application.admin_discord_id
        if not is_admin:
            await ctx.send("You don't have permission to use this command.")
        return is_admin

    def is_not_banned(self, ctx: commands.Context[Any]) -> bool:
        return ctx.author.id not in self._app.userdata.get(UserdataFile.BANNED_USERS)
