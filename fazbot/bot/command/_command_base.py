# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from discord.ext.commands import Context


class CommandBase(ABC):

    def __init__(self, ctx: Context[Any]) -> None:
        self._ctx = ctx

    async def _respond(self, *args: Any, **kwargs: Any) -> None:
        await self._ctx.send(*args, **kwargs)
