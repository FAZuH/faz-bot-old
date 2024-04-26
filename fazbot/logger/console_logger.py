from loguru import logger


class ConsoleLogger:

    _is_debug = False
    _is_logger = logger

    @classmethod
    def success(cls, message: str) -> None:
        """ Logs a success message. Used for successful operations. """
        if cls._is_debug:
            cls._is_logger.success(message)

    @classmethod
    def info(cls, message: str) -> None:
        """ Logs an informational message. Used for general information. """
        if cls._is_debug:
            cls._is_logger.info(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """ Logs a debug message. Used for debugging purposes. """
        if cls._is_debug:
            cls._is_logger.debug(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """ Logs a warning message. Used for non-critical issues. """
        if cls._is_debug:
            cls._is_logger.warning(message)

    @classmethod
    def exception(cls, message: str) -> None:
        """ Logs an exception message. Used for critical issues that doesn't cause the program to stop. """
        cls._is_logger.exception(message)


    @classmethod
    def get_is_debug(cls) -> bool:
        return cls._is_debug

    @classmethod
    def set_is_debug(cls, is_debug: bool) -> None:
        cls._is_debug = is_debug
