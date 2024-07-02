class BotError(BaseException):
    """Base exception for all exceptions in fazbot bot module"""

class CommandFailure(BotError):
    pass
