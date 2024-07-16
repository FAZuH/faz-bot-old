import os
from typing import Callable

from dotenv import load_dotenv

from ._asset import Asset


class Properties:

    # Application constants
    AUTHOR = "FAZuH"
    VERSION = "0.0.1"
    ASSET_DIR = "asset"
    LOG_DIR = "./logs"

    # .env
    DISCORD_BOT_TOKEN: str

    ADMIN_DISCORD_ID: int
    DEV_SERVER_ID: int

    DISCORD_LOG_WEBHOOK: str
    DISCORD_STATUS_WEBHOOK: str

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str

    FAZDB_DB_NAME: str
    FAZBOT_DB_NAME: str
    MANGA_NOTIFY_DB_NAME: str

    FAZBOT_DB_MAX_RETRIES: int
    FAZDB_DB_MAX_RETRIES: int
    MANGA_NOTIFY_DB_MAX_RETRIES: int

    # Additional application property classes
    ASSET: Asset

    @classmethod
    def setup(cls) -> None:
        """Bootstraps application properties."""
        cls.__read_env()
        cls.ASSET = Asset(cls.ASSET_DIR)
        cls.ASSET.read_all()

    @classmethod
    def __read_env(cls) -> None:
        load_dotenv()
        cls.DISCORD_BOT_TOKEN = cls.__must_get_env("DISCORD_BOT_TOKEN")

        cls.ADMIN_DISCORD_ID = cls.__must_get_env("ADMIN_DISCORD_ID", int)
        cls.DEV_SERVER_ID = cls.__must_get_env("DEV_SERVER_ID", int)

        cls.DISCORD_LOG_WEBHOOK = cls.__must_get_env("DISCORD_LOG_WEBHOOK")
        cls.DISCORD_STATUS_WEBHOOK = cls.__must_get_env("DISCORD_STATUS_WEBHOOK")

        cls.MYSQL_HOST = cls.__must_get_env("MYSQL_HOST")
        cls.MYSQL_PORT = cls.__must_get_env("MYSQL_PORT", int)
        cls.MYSQL_USERNAME = cls.__must_get_env("MYSQL_USER")
        cls.MYSQL_PASSWORD = cls.__must_get_env("MYSQL_PASSWORD")

        cls.FAZBOT_DB_NAME = cls.__must_get_env("MYSQL_FAZBOT_DATABASE")
        cls.FAZDB_DB_NAME = cls.__must_get_env("MYSQL_FAZDB_DATABASE")
        cls.MANGA_NOTIFY_DB_NAME = cls.__must_get_env("MANGA_NOTIFY_DB_NAME")

        cls.FAZBOT_DB_MAX_RETRIES = cls.__must_get_env("FAZBOT_DB_MAX_RETRIES", int)
        cls.FAZDB_DB_MAX_RETRIES = cls.__must_get_env("FAZDB_DB_MAX_RETRIES", int)
        cls.MANGA_NOTIFY_DB_MAX_RETRIES = cls.__must_get_env("MANGA_NOTIFY_DB_MAX_RETRIES", int)

    @staticmethod
    def __must_get_env[T](key: str, type_strategy: Callable[[str], T] = str) -> T:
        try:
            env = os.getenv(key)
            return type_strategy(env)  # type: ignore
        except ValueError:
            raise ValueError(f"Failed parsing environment variable {key} into type {type_strategy}")
