from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from . import ConsoleLogger, DiscordLogger, PerformanceLogger


class Logger(Protocol):
    @property
    def console_logger(cls) -> ConsoleLogger: ...
    @property
    def discord_logger(cls) -> DiscordLogger: ...
    @property
    def performance_logger(cls) -> PerformanceLogger: ...
