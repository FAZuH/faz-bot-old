from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from . import Heartbeat, HeartbeatTask

if TYPE_CHECKING:
    from .task import Task
    from fazbot import App


class SimpleHeartbeat(Thread, Heartbeat):

    def __init__(self, app: App) -> None:
        super().__init__(target=self.run, daemon=True)
        self._app = app
        self._tasks: list[HeartbeatTask] = []

    def start(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()

    @property
    def tasks(self) -> list[HeartbeatTask]:
        return self._tasks

    def _add_task(self, task: Task) -> None:
        self._tasks.append(HeartbeatTask(task, self._app.logger))
