from __future__ import annotations
from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING, Any

from yaml import dump, load, Dumper, Loader

from fazbot import Constants

if TYPE_CHECKING:
    from pathlib import Path


class _ConfigNode(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config


class Config:

    def __init__(self) -> None:
        self._fp = Path(Constants.CONFIG_FP)
        self._config: dict[str, Any] = {}

    def load(self) -> None:
        with open(self._fp, "r") as stream:
            self._config = load(stream, Loader=Loader)
        self._application = Config._Application(self._config["application"])
        self._logging = Config._Logging(self._config["logging"])
        self._secret = Config._Secret(self._config["secret"])

    def save(self) -> None:
        with open(self._fp, "w") as stream:
            dump(self._config, stream, Dumper)

    @property
    def application(self) -> Config._Application: return self._application

    @property
    def logging(self) -> Config._Logging: return self._logging

    @property
    def secret(self) -> Config._Secret: return self._secret


    class _Application(_ConfigNode):
        @property
        def debug(self) -> bool: return bool(self._config["debug"])
        @property
        def admin_discord_id(self) -> int: return int(self._config["admin_discord_id"])

    class _Logging(_ConfigNode):
        @property
        def error_log_file(self) -> str: return self._config["error_log_file"]
        @property
        def error_log_webhook(self) -> str: return self._config["error_log_webhook"]
        @property
        def status_report_webhook(self) -> str: return self._config["status_report_webhook"]

    class _Secret(_ConfigNode):
        def __init__(self, config: dict[str, Any]) -> None:
            super().__init__(config)
            self._discord = Config._Secret._Discord(config["discord"])
            self._fazbot = Config._Secret._Database(config["fazbot"])
            self._wynndb = Config._Secret._Database(config["wynndb"])
        @property
        def discord(self) -> Config._Secret._Discord: return self._discord
        @property
        def fazbot(self) -> Config._Secret._Database: return self._fazbot
        @property
        def wynndb(self) -> Config._Secret._Database: return self._wynndb

        class _Discord(_ConfigNode):
            @property
            def bot_client_secret(self) -> str: return self._config["bot_client_secret"]
            @property
            def bot_client_id(self) -> int: return int(self._config["bot_client_id"])
            @property
            def bot_token(self) -> str: return self._config["bot_token"]

        class _Database(_ConfigNode):
            @property
            def db_username(self) -> str: return self._config["db_username"]
            @property
            def db_password(self) -> str: return self._config["db_password"]
            @property
            def db_max_retries(self) -> int: return int(self._config["db_max_retries"])
            @property
            def db_schema_name(self) -> str: return self._config["db_schema_name"]
