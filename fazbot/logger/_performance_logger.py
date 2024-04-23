from datetime import datetime, timedelta
from functools import wraps
from threading import Lock
from time import perf_counter
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar

P = ParamSpec('P')
T = TypeVar('T')


class PerformanceLogger:

    def __init__(self) -> None:
        self._data: dict[str, list[tuple[datetime, timedelta]]] = {}
        """{name: [(callDatetime: dallDuration)]}"""
        self._lock = Lock()

        self._MAX_CACHE = 1_000
        """Max amount of cache for each name. If exceeded, the oldest data will be removed."""

    def bind_async(self, callable: Callable[P, Awaitable[T]], name: None | str = None) -> Callable[P, Coroutine[Any, Any, T]]:
        """Decorator to record the duration of an async method. The duration will be recorded in `timedelta`."""
        if name is None:
            name = callable.__qualname__

        self._data[name] = []

        @wraps(callable)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            t1 = perf_counter()
            res = await callable(*args, **kwargs)
            td = timedelta(seconds=perf_counter() - t1)
            now = datetime.now()

            with self._lock:
                list_ = self._data[name]  # get reference
                list_.append((now, td))
                if len(list_) > self._MAX_CACHE:
                    # NOTE: List is ordered by oldest to newest. list.pop(0) removes the oldest data
                    list_.pop(0)
            return res

        return wrapped

    def bind_sync(self, callable: Callable[P, T], name: None | str = None) -> Callable[P, T]:
        """Decorator to record the duration of an async method. The duration will be recorded in `timedelta`."""
        if name is None:
            name = callable.__qualname__

        self._data[name] = []

        @wraps(callable)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            t1 = perf_counter()
            res = callable(*args, **kwargs)
            td = timedelta(seconds=perf_counter() - t1)
            now = datetime.now()

            with self._lock:
                list_ = self._data[name]  # get reference
                list_.append((now, td))
                if len(list_) > self._MAX_CACHE:
                    # NOTE: List is ordered by oldest to newest. list.pop(0) removes the oldest data
                    list_.pop(0)
            return res

        return wrapped

    def get_average(self, name: str) -> float:
        """Get average duration of calls in seconds. If no data, return 0."""
        with self._lock:
            if name in self._data and len(self._data[name]) > 0:
                sum_duration_s = sum(item[1].total_seconds() for item in self._data[name])
                return sum_duration_s / len(self._data[name])
            else:
                return 0

    def get_recent(self, timedelta: timedelta, name: str) -> list[timedelta]:
        """Get all calls within `timedelta` from now. If no data, return empty list."""
        with self._lock:
            if name in self._data:
                now = datetime.now()
                return [item[1] for item in self._data[name] if (now - item[0]) < timedelta]
            else:
                return []
