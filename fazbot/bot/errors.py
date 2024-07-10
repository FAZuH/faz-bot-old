from nextcord import ApplicationCheckFailure


class BotException(BaseException):
    """Base exception for all exceptions in fazbot bot module"""

    # def __init__(self, *args):
    #     if message:
    #         message = f"{self.__class__.__doc__}\n{message}"
    #     else:
    #         message = self.__class__.__doc__
    #     super().__init__(message, args)


class CommandException(BotException, ApplicationCheckFailure):
    pass

class ParseException(CommandException):
    pass

class BadCommandArgument(CommandException):
    pass
