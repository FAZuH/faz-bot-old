# pyright: reportMissingTypeStubs=false
from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from nextcord import Guild
    from nextcord.ext.commands import Bot as Bot_
    from . import Checks


class Bot(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def bot(self) -> Bot_:...
    @property
    def checks(self) -> Checks: ...
    @property
    def synced_guilds(self) -> list[Guild]: ...
