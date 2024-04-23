from . import (
    ConsoleLogger,
    DiscordLogger,
    PerformanceLogger,
    Logger
)


class FazBotLogger(Logger):

    def __init__(
        self,
        error_log_webhook: str ,
        is_debug: bool = False,
        admin_discord_id: int | None = None
    )  -> None:
        self._console_logger = ConsoleLogger(is_debug)
        self._discord_logger = DiscordLogger(self._console_logger, error_log_webhook, admin_discord_id)
        self._performance_logger = PerformanceLogger()

    @property
    def console_logger(cls) -> ConsoleLogger:
        return cls._console_logger

    @property
    def discord_logger(cls) -> DiscordLogger:
        return cls._discord_logger

    @property
    def performance_logger(cls) -> PerformanceLogger:
        return cls._performance_logger
