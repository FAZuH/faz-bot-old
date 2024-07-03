from nextcord import ApplicationCheckFailure


class BotException(BaseException):
    """Base exception for all exceptions in fazbot bot module"""

class CommandException(BotException, ApplicationCheckFailure):
    pass

class ParseException(CommandException):
    pass

class BadCommandArgument(CommandException):
    pass
