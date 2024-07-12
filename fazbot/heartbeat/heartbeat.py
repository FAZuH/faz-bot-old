from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING

from ._heartbeat_task import HeartbeatTask
from .task import RequestQueue, ResponseQueue, TaskApiRequest, TaskDbInsert

if TYPE_CHECKING:
    from .task import ITask
    from fazdb.api import WynnApi
    from fazdb.db.fazdb import FazdbDatabase


class Heartbeat(Thread):

    def __init__(self, api: WynnApi, db: FazdbDatabase) -> None:
        super().__init__(target=self.run, daemon=True)
        self._tasks: list[HeartbeatTask] = []

        request_queue = RequestQueue()
        response_queue = ResponseQueue()
        api_request = TaskApiRequest(api, request_queue, response_queue)
        db_insert = TaskDbInsert(api, db, request_queue, response_queue)

        self._add_task(api_request)
        self._add_task(db_insert)

    def start(self) -> None:
        for task in self._tasks:
            task.start()

    def stop(self) -> None:
        for task in self._tasks:
            task.cancel()

    def _add_task(self, task: ITask) -> None:
        self._tasks.append(HeartbeatTask(task))
