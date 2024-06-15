from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Callable

import dateparser

if TYPE_CHECKING:
    from nextcord import Guild, PartialMessageable, Thread, User
    from nextcord.abc import GuildChannel, PrivateChannel
    from nextcord.ext.commands import Bot


class Utils:

    @staticmethod
    async def must_get_channel(bot: Bot, channel_id: str) -> GuildChannel | Thread | PrivateChannel | PartialMessageable:
        return await Utils.must_get_id(bot.get_channel, channel_id)

    @staticmethod
    async def must_get_guild(bot: Bot, guild_id: str) -> Guild:
        return await Utils.must_get_id(bot.get_guild, guild_id)

    @staticmethod
    async def must_get_user(bot: Bot, user_id: str) -> User:
        return await Utils.must_get_id(bot.get_user, user_id)

    @staticmethod
    async def must_get_id[T](get_strategy: Callable[[int], T | None], id_str: str) -> T:
        try:
            id_int = int(id_str)
        except ValueError:
            raise ValueError(f"Failed parsing {id_str} into an integer.")
        if not (ret := get_strategy(id_int)):
            raise ValueError(f"Failed getting object from ID {id_str}")
        return ret

    @staticmethod
    def must_parse_date_string(datestr: str) -> datetime:
        date = dateparser.parse(datestr)
        if not date:
            raise ValueError(f"Failed parsing date string {datestr}")
        return date
