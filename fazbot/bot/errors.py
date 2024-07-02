from nextcord import ApplicationCheckFailure


class BotError(BaseException):
    """Base exception for all exceptions in fazbot bot module"""

class CommandFailure(BotError, ApplicationCheckFailure):
    pass

class ParseError(BotError):
    pass
