from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from discord import Client
    from discord.app_commands import CommandTree


class Bot(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def client(self) -> Client: ...
    @property
    def command_tree(self) -> CommandTree: ...
