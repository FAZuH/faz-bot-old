from loguru import logger


class ConsoleLogger:

    _logger = logger

    @classmethod
    def success(cls, message: str) -> None:
        """ Logs a success message. Used for successful operations. """
        cls._logger.success(message)

    @classmethod
    def info(cls, message: str) -> None:
        """ Logs an informational message. Used for general information. """
        cls._logger.info(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """ Logs a debug message. Used for debugging purposes. """
        cls._logger.debug(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """ Logs a warning message. Used for non-critical issues. """
        cls._logger.warning(message)

    @classmethod
    def exception(cls, message: str) -> None:
        """ Logs an exception message. Used for critical issues that doesn't cause the program to stop. """
        cls._logger.exception(message)
