from pathlib import Path

from fazbot import Constants
from fazbot.enum import AssetImageFile


class ImageAsset:

    def __init__(self) -> None:
        self._type = AssetImageFile
        self._dir = Path(Constants.ASSET_IMAGE_DIR)
        self._files: dict[AssetImageFile, bytes] = {}

    def load(self) -> None:
        for fp in self._type:
            with open(self._get_fp(fp), "r") as file:
                self._files[fp] = file.buffer.read()

    def save(self) -> None:
        for fp, data in self._files.items():
            with open(self._get_fp(fp), "w") as file:
                file.buffer.write(data)

    def get(self, asset: AssetImageFile) -> bytes:
        return self._files[asset]

    def set(self, asset: AssetImageFile, data: bytes) -> None:
        self._files[asset] = data

    @property
    def files(self) -> dict[AssetImageFile, bytes]:
        return self._files

    @property
    def enum(self) -> type[AssetImageFile]:
        return self._type

    def _get_fp(self, path: AssetImageFile) -> Path:
        return self._dir / path.value
