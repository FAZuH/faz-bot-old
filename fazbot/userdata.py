from json import dump, load
from pathlib import Path
from typing import Any

from fazbot import Constants
from fazbot.enum import UserdataFile

FromJson = dict[str, Any] | list[Any]


class Userdata:

    def __init__(self) -> None:
        self._type = UserdataFile
        self._dir = Path(Constants.USERDATA_DIR)
        self._files: dict[UserdataFile, FromJson] = {}

    def load(self) -> None:
        for fp in self._type:
            with open(self._get_fp(fp), "r") as file:
                self._files[fp] = load(file)

    def save(self) -> None:
        for fp, data in self._files.items():
            with open(self._get_fp(fp), "w") as file:
                dump(data, file)

    def get(self, asset: UserdataFile) -> FromJson:
        return self._files[asset]

    def set(self, asset: UserdataFile, data: FromJson) -> None:
        self._files[asset] = data

    @property
    def files(self) -> dict[UserdataFile, FromJson]:
        return self._files


    def _get_fp(self, path: UserdataFile) -> Path:
        return self._dir / path.value
