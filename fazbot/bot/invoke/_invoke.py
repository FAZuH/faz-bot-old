from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from ._asset import Asset

if TYPE_CHECKING:
    from nextcord import Embed, File, Interaction
    from .. import Bot


class Invoke(ABC):

    def __init__(self, bot: Bot, interaction: Interaction[Any]) -> None:
        self._bot = bot
        self._interaction = interaction

    @abstractmethod
    async def run(self): ...

    @staticmethod
    def _set_embed_thumbnail_with_asset(embed: Embed, filename: str) -> None:
        embed.set_thumbnail(url=f"attachment://{filename}")

    @staticmethod
    def _get_from_assets(assets: dict[str, File], key: str) -> Asset:
        """Helper method to get an asset.
        Normally only be used inside `_set_assets()`

        Args:
            assets (dict[str, File]): asset dictionary. Normally obtained from `_set_assets()`
            key (str): The file name of the asset.

        Returns:
            Asset: The asset object containing File object and the file name
        """
        file = assets.get(key, None)
        if not file:
            raise KeyError(f"Asset with key {key} doesn't exist.")
        asset = Asset(file, key)
        return asset

    @classmethod
    def set_assets(cls, assets: dict[str, File]) -> None:
        ...

