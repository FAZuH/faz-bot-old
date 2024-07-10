from __future__ import annotations
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Any, Awaitable, Callable, Iterable

from loguru import logger


class RetryHandler:

    @staticmethod
    def async_decorator[T, **P](
        max_retries: int,
        exceptions: type[BaseException] | tuple[type[BaseException]]
    ) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
        """ Retries the wrapped function/method `max_retries` times if the exceptions listed in `exceptions` are thrown """
        def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
            @wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                for _ in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions:
                        pass
                with logger.catch(level="ERROR", reraise=True):
                    return await func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def decorator[T, **P](
        max_retries: int,
        exceptions: type[BaseException] | tuple[type[BaseException]]
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """ Retries the wrapped function/method `max_retries` times if the exceptions listed in `exceptions` are thrown """
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                for _ in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except exceptions:
                        pass
                with logger.catch(level="ERROR", reraise=True):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def register(
            func: Callable[..., Any | Awaitable[Any]] | Iterable[Callable[..., Any | Awaitable[Any]]],
            max_retries: int,
            exceptions: type[BaseException] | tuple[type[BaseException]]
        ) -> None:
        """ Register object method(s) to be wrapped with an error handler """
        if isinstance(func, Iterable):
            for f in func:
                RetryHandler.register(f, max_retries, exceptions)
            return

        if iscoroutinefunction(func):
            wrapper = RetryHandler.async_decorator(max_retries, exceptions)
        else:
            wrapper = RetryHandler.decorator(max_retries, exceptions)

        wrapped_func = wrapper(func)

        setattr(wrapped_func, "__self__", func.__self__)  # type: ignore
        setattr(func.__self__, func.__name__, wrapped_func)  # type: ignore
