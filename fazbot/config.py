from __future__ import annotations
from json import load as json_load
from typing import TYPE_CHECKING, Any

from yaml import load as yaml_load, Loader

if TYPE_CHECKING:
    from pathlib import Path


class Config:

    def __init__(self, config_dir_fp: Path) -> None:
        self._config_fp = config_dir_fp
        self._application: Config._Application
        self._logging: Config._Logging
        self._secret: Config._Secret

    def load_config(self) -> None:
        with open(self._config_fp / "config.yml", "r") as stream:
            config1 = yaml_load(stream, Loader=Loader)
        self._application = Config._Application(config1["application"])
        self._logging = Config._Logging(config1["logging"])
        self._secret = Config._Secret(config1["secret"])

        with open(self._config_fp / "authorized_guilds.json") as stream:
            config2 = json_load(stream)
        self._authorized_guilds = config2

    # TODO: Implement save_config

    @property
    def application(self) -> Config._Application: return self._application

    @property
    def logging(self) -> Config._Logging: return self._logging

    @property
    def secret(self) -> Config._Secret: return self._secret

    @property
    def authorized_guilds(self) -> list[int]: return self._authorized_guilds

    class _Application:
        def __init__(self, config: dict[str, Any]) -> None: self._config = config

        @property
        def debug(self) -> bool: return bool(self._config["debug"])

        @property
        def admin_discord_id(self) -> int: return int(self._config["admin_discord_id"])

    class _Logging:
        def __init__(self, config: dict[str, Any]) -> None: self._config = config

        @property
        def error_log_file(self) -> str: return self._config["error_log_file"]

        @property
        def error_log_webhook(self) -> str: return self._config["error_log_webhook"]

        @property
        def status_report_webhook(self) -> str: return self._config["status_report_webhook"]

    class _Secret:
        def __init__(self, config: dict[str, Any]) -> None:
            self._config = config
            self._discord = Config._Secret._Discord(config["discord"])
            self._fazbot = Config._Secret._Database(config["fazbot"])
            self._wynndb = Config._Secret._Database(config["wynndb"])

        @property
        def discord(self) -> Config._Secret._Discord: return self._discord

        @property
        def fazbot(self) -> Config._Secret._Database: return self._fazbot

        @property
        def wynndb(self) -> Config._Secret._Database: return self._wynndb

        class _Discord:
            def __init__(self, config: dict[str, Any]) -> None: self._config = config

            @property
            def bot_client_secret(self) -> str: return self._config["bot_client_secret"]

            @property
            def bot_client_id(self) -> int: return int(self._config["bot_client_id"])

            @property
            def bot_token(self) -> str: return self._config["bot_token"]

        class _Database:
            def __init__(self, config: dict[str, Any]) -> None: self._config = config

            @property
            def db_username(self) -> str: return self._config["db_username"]

            @property
            def db_password(self) -> str: return self._config["db_password"]

            @property
            def db_max_retries(self) -> int: return int(self._config["db_max_retries"])

            @property
            def db_schema_name(self) -> str: return self._config["db_schema_name"]
