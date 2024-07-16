from __future__ import annotations
from datetime import datetime
from typing import Any, Callable, TYPE_CHECKING

import dateparser

from .errors import ParseFailure

if TYPE_CHECKING:
    from nextcord import Guild, PartialMessageable, Thread, User
    from nextcord.abc import GuildChannel, PrivateChannel
    from nextcord.ext.commands import Bot


class Utils:

    @staticmethod
    async def must_get_channel(bot: Bot, channel_id: Any) -> GuildChannel | Thread | PrivateChannel | PartialMessageable:
        return await Utils.must_get_id(bot.get_channel, channel_id)

    @staticmethod
    async def must_get_sendable_channel(bot: Bot, channel_id: Any) -> GuildChannel | Thread | PrivateChannel | PartialMessageable:
        channel = await Utils.must_get_id(bot.get_channel, channel_id)
        if not hasattr(channel, "send"):
            raise ParseFailure(f"Channel with id {channel_id} does not support sending messages.")
        return channel

    @staticmethod
    async def must_get_guild(bot: Bot, guild_id: Any) -> Guild:
        return await Utils.must_get_id(bot.get_guild, guild_id)

    @staticmethod
    async def must_get_user(bot: Bot, user_id: Any) -> User:
        return await Utils.must_get_id(bot.get_user, user_id)

    @staticmethod
    async def must_get_id[T](get_strategy: Callable[[int], T | None], id_: Any) -> T:
        try:
            parsed_id = int(id_)
        except ParseFailure:
            raise ParseFailure(f"Failed parsing {id_} into an integer.")
        if not (ret := get_strategy(parsed_id)):
            raise ParseFailure(f"Failed getting object from ID {id_}")
        return ret

    @staticmethod
    def must_parse_date_string(datestr: str) -> datetime:
        date = dateparser.parse(datestr)
        if not date:
            raise ParseFailure(f"Failed parsing date string {datestr}")
        return date
