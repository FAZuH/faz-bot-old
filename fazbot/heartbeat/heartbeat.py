from __future__ import annotations
from typing import Protocol


class Heartbeat(Protocol):
    """ <<interface>> """
    def start(self) -> None: ...
    def stop(self) -> None: ...
