from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Model(ABC):

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Model: ...
