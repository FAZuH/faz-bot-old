from loguru import logger


class ConsoleLogger:

    def __init__(self, is_debug: bool) -> None:
        self._is_debug = is_debug
        self._logger = logger

    def success(self, message: str) -> None:
        """ Logs a success message. Used for successful operations. """
        if self._is_debug:
            self._logger.success(message)

    def info(self, message: str) -> None:
        """ Logs an informational message. Used for general information. """
        if self._is_debug:
            self._logger.info(message)

    def debug(self, message: str) -> None:
        """ Logs a debug message. Used for debugging purposes. """
        if self._is_debug:
            self._logger.debug(message)

    def warning(self, message: str) -> None:
        """ Logs a warning message. Used for non-critical issues. """
        if self._is_debug:
            self._logger.warning(message)

    def exception(self, message: str) -> None:
        """ Logs an exception message. Used for critical issues that doesn't cause the program to stop. """
        self._logger.exception(message)

    @property
    def is_debug(self) -> bool:
        return self._is_debug
