from . import (
    ConsoleLogger,
    DiscordLogger,
    Logger
)


class FazBotLogger(Logger):

    def __init__(
        self,
        error_log_webhook: str ,
        admin_discord_id: int | None = None
    )  -> None:
        self._console_logger = ConsoleLogger()
        self._discord_logger = DiscordLogger(error_log_webhook, admin_discord_id, self._console_logger)

    @property
    def console(cls) -> ConsoleLogger:
        return cls._console_logger

    @property
    def discord(cls) -> DiscordLogger:
        return cls._discord_logger
