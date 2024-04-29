from functools import wraps
from inspect import iscoroutinefunction
from typing import Awaitable, Callable, ParamSpec, TypeVar, Iterable

from fazbot.logger import ConsoleLogger

T = TypeVar('T')
U = TypeVar('U')
P = ParamSpec('P')


class ErrorHandler:

    @staticmethod
    def retry_decorator(max_retries: int, exceptions: type[BaseException] | Iterable[type[BaseException]]) -> Callable[[Callable[P, T | Awaitable[T]]], Callable[P, Awaitable[T]]]:
        """ Retries the wrapped function/method `times` times if the exceptions listed in `exceptions` are thrown """
        def decorator(f: Callable[P, T | Awaitable[T]]) -> Callable[P, Awaitable[T]]:
            @wraps(f)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                for _ in range(max_retries):
                    try:
                        return await ErrorHandler._must_return(f)
                    except exceptions:  # type: ignore
                        ConsoleLogger.exception(
                                f"{f.__qualname__} failed. Retrying..."
                                f"args:{str(args)[:30]}\n"
                                f"kwargs:{str(kwargs)[:30]}"
                        )
                return await ErrorHandler._must_return(f)
            return wrapper
        return decorator

    @staticmethod
    async def _must_return(func: Callable[..., T | Awaitable[T]]) -> T:
        if iscoroutinefunction(func):
            return await func()
        return func()  # type: ignore
