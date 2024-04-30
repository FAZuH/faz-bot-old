from json import dump, load
from pathlib import Path
from typing import Any

from fazbot import Constants
from fazbot.enum import UserdataFile

JsonType = dict[str, Any] | list[Any]


class Userdata:

    def __init__(self) -> None:
        self._type = UserdataFile
        self._dir = Path(Constants.USERDATA_DIR)
        self._files: dict[UserdataFile, JsonType] = {}

    def load(self) -> None:
        for fp in self._type:
            with open(self._get_fp(fp), "r") as file:
                self._files[fp] = load(file)

    def save(self, userdata: UserdataFile | None = None) -> None:
        if userdata:
            with open(self._get_fp(userdata), "w") as file:
                dump(self._files[userdata], file)
            return
        for fp, data in self._files.items():
            with open(self._get_fp(fp), "w") as file:
                dump(data, file)

    def get(self, userdata: UserdataFile) -> JsonType:
        return self._files[userdata]

    def set(self, userdata: UserdataFile, data: JsonType) -> None:
        self._files[userdata] = data

    @property
    def files(self) -> dict[UserdataFile, JsonType]:
        return self._files

    @property
    def enum(self) -> type[UserdataFile]:
        return self._type

    def _get_fp(self, path: UserdataFile) -> Path:
        return self._dir / path.value
