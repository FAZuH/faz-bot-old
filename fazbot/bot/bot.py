from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from nextcord.ext.commands import Bot as Client

    from fazbot import App, Logger

    from . import AssetManager, Checks, Events
    from .cog import CogCore


class Bot(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    async def on_ready_setup(self) -> None: ...
    @property
    def asset_manager(self) -> AssetManager: ...
    @property
    def cogs(self) -> CogCore: ...
    @property
    def core(self) -> App: ...
    @property
    def client(self) -> Client: ...
    @property
    def checks(self) -> Checks: ...
    @property
    def events(self) -> Events: ...
    @property
    def logger(self) -> Logger: ...
