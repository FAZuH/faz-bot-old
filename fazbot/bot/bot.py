# pyright: reportMissingTypeStubs=false
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from nextcord.ext.commands import Bot as Client

    from fazbot import Core

    from . import Checks, CogCore


class Bot(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def setup(self) -> None: ...
    @property
    def checks(self) -> Checks: ...
    @property
    def client(self) -> Client: ...
    @property
    def cogs(self) -> CogCore: ...
    @property
    def core(self) -> Core: ...
