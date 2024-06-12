from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from nextcord.ext.commands import Bot as Client

    from fazbot import Core

    from . import Checks, Events
    from .cog import CogCore
    from .invoke import AssetManager


class Bot(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def setup(self) -> None: ...
    @property
    def asset_manager(self) -> AssetManager: ...
    @property
    def cogs(self) -> CogCore: ...
    @property
    def core(self) -> Core: ...
    @property
    def client(self) -> Client: ...
    @property
    def checks(self) -> Checks: ...
    @property
    def event(self) -> Events: ...

