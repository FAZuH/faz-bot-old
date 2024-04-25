from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from fazbot import ImageAsset, Bot, Config, Heartbeat, Logger, Userdata


class App(Protocol):
    """<<interface>>"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def asset(self) -> ImageAsset: ...
    @property
    def bot(self) -> Bot: ...
    @property
    def config(self) -> Config: ...
    @property
    def heartbeat(self) -> Heartbeat: ...
    @property
    def logger(self) -> Logger: ...
    @property
    def userdata(self) -> Userdata: ...
