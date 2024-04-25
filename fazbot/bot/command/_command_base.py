# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any

from fazbot import ImageAsset

if TYPE_CHECKING:
    from discord import Message
    from discord.ext.commands import Context


class CommandBase(ABC):

    _asset: ImageAsset

    def __init__(self, ctx: Context[Any]) -> None:
        self._ctx = ctx

    @classmethod
    def get_asset(cls) -> ImageAsset:
        return cls._asset

    @classmethod
    def set_asset(cls, asset: ImageAsset) -> None:
        cls._asset = asset

    async def _respond(self, *args: Any, **kwargs: Any) -> Message:
        return await self._ctx.send(*args, **kwargs)
