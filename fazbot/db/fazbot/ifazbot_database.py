from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .model import BaseModel
    from .repository import BannedUserRepository, WhitelistedGuildRepository


class IFazBotDatabase(Protocol):
    def __init__(self, driver: str, user: str, password: str, host: str, database: str) -> None: ...
    @property
    def banned_user_repository(self) -> BannedUserRepository: ...
    @property
    def whitelisted_guild_repository(self) -> WhitelistedGuildRepository: ...
    @property
    def base_model(self) -> BaseModel: ...
