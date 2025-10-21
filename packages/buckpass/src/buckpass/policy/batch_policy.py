from __future__ import annotations

from enum import Enum
from typing import Generic, TypeVar

from typing_extensions import override

from buckpass.core import IntGTZ, Policy, Submitter


class WorkerEvent(Enum):
    START = 0
    END = 1


WorkerId = TypeVar("WorkerId")
Args = TypeVar("Args")


class BatchPolicy(
    Policy[tuple[WorkerId, WorkerEvent]],
    Generic[WorkerId, Args],
):
    __args: Args
    __max_runs: IntGTZ
    __batch_size: IntGTZ
    __submitter: Submitter[WorkerId, Args]
    __submitted_workers: set[WorkerId]
    __running_workers: set[WorkerId]
    __total_submitted: int = 0

    def __init__(
        self,
        args: Args,
        max_runs: IntGTZ,
        batch_size: IntGTZ,
        submitter: Submitter[WorkerId, Args],
    ) -> None:
        super().__init__()

        self.__args = args
        self.__max_runs = max_runs
        self.__batch_size = batch_size
        self.__submitter = submitter
        self.__submitted_workers = set()
        self.__running_workers = set()

        self.__fill()

    @override
    def update(self, event: tuple[WorkerId, WorkerEvent]) -> None:
        (job_id, job_event_type) = event

        match job_event_type:
            case WorkerEvent.START:
                if job_id in self.__submitted_workers:
                    self.__submitted_workers.remove(job_id)
                    self.__running_workers.add(job_id)
            case WorkerEvent.END:
                if job_id in self.__submitted_workers:
                    self.__submitted_workers.remove(job_id)
                if job_id in self.__running_workers:
                    self.__running_workers.remove(job_id)

        self.__fill()

    def __fill(self) -> None:
        while (
            len(self.__submitted_workers) + len(self.__running_workers)
            < self.__batch_size
            and self.__total_submitted < self.__max_runs
        ):
            worker_id = self.__submitter.submit(self.__args)
            self.__submitted_workers.add(worker_id)
            self.__total_submitted += 1

    def is_terminated(self) -> bool:
        return (
            len(self.__submitted_workers) == 0
            and self.__total_submitted >= self.__max_runs
        )
