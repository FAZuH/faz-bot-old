from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from . import Heartbeat, HeartbeatTask

if TYPE_CHECKING:
    from .task import Task
    from fazbot import Core


class SimpleHeartbeat(Thread, Heartbeat):

    def __init__(self, app: Core) -> None:
        super().__init__(target=self.run, daemon=True)
        self._app = app
        self._tasks: list[HeartbeatTask] = []

    def start(self) -> None:
        self._app.logger.console.info("Starting Heartbeat...")
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        self._app.logger.console.info("Stopping Heartbeat...")
        for task in self._tasks:
            task.cancel()

    @property
    def tasks(self) -> list[HeartbeatTask]:
        return self._tasks

    def _add_task(self, task: Task) -> None:
        self._tasks.append(HeartbeatTask(task, self._app.logger))
