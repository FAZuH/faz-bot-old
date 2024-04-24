from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from discord import Interaction


class CommandBase(ABC):

    def __init__(self, interaction: Interaction) -> None:
        self._interaction = interaction

    async def _respond(self, *args: Any, **kwargs: Any) -> None:
        await self._interaction.response.send_message(*args, **kwargs)

    async def _defer(self, ephemeral: bool = False, thinking: bool = False):
        await self._interaction.response.defer(ephemeral=ephemeral, thinking=thinking)
