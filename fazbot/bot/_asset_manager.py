from __future__ import annotations
from asyncio import wait
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

from nextcord import File

from .invoke import (
    InvokeConvertEmerald,
    InvokeCraftedProbability,
    InvokeIngredientProbability,
)

if TYPE_CHECKING:
    from . import Bot


class AssetManager:
    """Class for managing assets for Invoke classes. Assets passed or set into the `asset` property
    is automatically converted into a dictionary of `dict[str, File]`. The converted asset is then 
    passed into class variables of Invoke subclasses automatically."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self.setup()

    def setup(self) -> None:
        self._assets = self._convert_asset_file_type(self._bot.app.properties.ASSET.files)
        InvokeConvertEmerald.set_assets(self._assets)
        InvokeCraftedProbability.set_assets(self._assets)
        InvokeIngredientProbability.set_assets(self._assets)

    def _convert_asset_file_type(self, assets: dict[Path, bytes]) -> dict[str, File]:
        assets_: dict[str, File] = {}
        for fp, asset in assets.items():
            fileio = BytesIO(asset)
            file = File(fileio, filename=fp.name)
            assets_[fp.name] = file
        return assets_
