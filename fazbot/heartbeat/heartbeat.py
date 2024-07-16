from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from loguru import logger

from ._heartbeat_task import HeartbeatTask
from .task import TaskMangaNotify

if TYPE_CHECKING:
    from .task import ITask
    from fazbot.app import App


class Heartbeat(Thread):

    def __init__(self, app: App) -> None:
        super().__init__(target=self.run, daemon=True)
        self._tasks: list[HeartbeatTask] = []

        self._task_manga_notify = TaskMangaNotify(app)
        self._add_task(self._task_manga_notify)

    def start(self) -> None:
        logger.info("Starting Heartbeat")
        for task in self._tasks:
            task.start()
        logger.success("Started Heartbeat")

    def stop(self) -> None:
        logger.info("Stopping Heartbeat")
        for task in self._tasks:
            task.cancel()
        logger.success("Stopped Heartbeat")

    def _add_task(self, task: ITask) -> None:
        self._tasks.append(HeartbeatTask(task))
