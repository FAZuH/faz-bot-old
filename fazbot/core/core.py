from __future__ import annotations
from contextlib import contextmanager
from typing import Generator, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Asset, Config
    from fazbot import Bot, Logger
    from fazbot.db.fazbot import IFazBotDatabase


class Core(Protocol):
    """<<interface>>"""
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def asset(self) -> Asset: ...
    @property
    def config(self) -> Config: ...
    @property
    def logger(self) -> Logger: ...
    @contextmanager
    def enter_bot(self) -> Generator[Bot]: ...
    @contextmanager
    def enter_fazbotdb(self) -> Generator[IFazBotDatabase]: ... 
