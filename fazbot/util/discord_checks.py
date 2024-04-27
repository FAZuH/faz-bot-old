from __future__ import annotations
from typing import TYPE_CHECKING, Any
from discord.ext import commands

from fazbot.enum import UserdataFile

if TYPE_CHECKING:
    from fazbot import Core


class DiscordChecks:

    def __init__(self, app: Core) -> None:
        self._app = app

    def is_admin(self, ctx: commands.Context[Any]) -> bool:
        is_admin = ctx.author.id == self._app.config.application.admin_discord_id
        return is_admin

    def is_not_banned(self, ctx: commands.Context[Any]) -> bool:
        is_not_banned = ctx.author.id not in self._app.userdata.get(UserdataFile.BANNED_USERS)
        return is_not_banned
