from functools import wraps
from typing import Any, Awaitable, Callable


class CacheUtil:

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def decorator[T, **P](self, func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = func.__name__
            if key not in self._cache:
                self._cache[key] = func(*args, **kwargs)
            return self._cache[key]
        return wrapper

    def async_decorator[T, **P](self, func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = func.__name__
            if key not in self._cache:
                self._cache[key] = await func(*args, **kwargs)
            return self._cache[key]
        return wrapper

    def register(self, obj: object, func: Callable[..., Any | Awaitable[Any]] | list[Callable[..., Any | Awaitable[Any]]]) -> None:
        if isinstance(func, list):
            for f in func:
                self.register(obj, f)
            return
        if not hasattr(obj, func.__name__):
            raise AttributeError(f"{obj.__class__.__name__} has no attribute '{func.__name__}'")
        setattr(obj, func.__name__, self.decorator(func))
