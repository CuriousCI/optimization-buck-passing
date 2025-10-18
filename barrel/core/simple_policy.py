from enum import Enum
from typing import Generic, TypeVar

from typing_extensions import override

import barrel


class WorkerEventType(Enum):
    START = 0
    END = 1


WorkerId = TypeVar("WorkerId")


class SimplePolicy(
    barrel.Policy[tuple[WorkerId, WorkerEventType]],
    Generic[WorkerId],
):
    __task_id: barrel.openbox.TaskId
    __pool_size: barrel.IntGEZ
    __submitter: barrel.core.Submitter[WorkerId, barrel.openbox.TaskId]
    __submitted_workers: set[WorkerId]
    __running_workers: set[WorkerId]

    def __init__(
        self,
        task_id: barrel.openbox.TaskId,
        pool_size: barrel.IntGEZ,
        submitter: barrel.Submitter[WorkerId, barrel.openbox.TaskId],
    ) -> None:
        super().__init__()

        self.__task_id = task_id
        self.__pool_size = pool_size
        self.__submitter = submitter
        for _ in range(pool_size):
            worker_id = self.__submitter.submit(self.__task_id)
            self.__submitted_workers.add(worker_id)

    @override
    def update(self, event: tuple[WorkerId, WorkerEventType]) -> None:
        (job_id, job_event_type) = event

        if job_id not in self.__running_workers:
            return

        match job_event_type:
            case WorkerEventType.START:
                self.__submitted_workers.remove(job_id)
                self.__running_workers.add(job_id)
            case WorkerEventType.END:
                # A worker might be cancelled before running
                self.__submitted_workers.remove(job_id)
                self.__running_workers.remove(job_id)

        while len(self.__submitted_workers) < self.__pool_size:
            worker_id = self.__submitter.submit(self.__task_id)
            self.__submitted_workers.add(worker_id)

    def workers(self) -> set[WorkerId]:
        return self.__submitted_workers | self.__running_workers
