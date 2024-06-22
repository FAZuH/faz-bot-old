from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nextcord import File


class Asset:

    def __init__(self, file: File, file_name: str) -> None:
        self._file = file
        self._file_name = file_name

    def get_file_to_send(self) -> File:
        return deepcopy(self._file)

    @property
    def filename(self) -> str:
        return self._file_name

