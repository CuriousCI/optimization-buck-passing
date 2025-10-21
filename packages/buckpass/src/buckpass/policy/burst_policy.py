from __future__ import annotations

from enum import Enum
from typing import Generic, TypeVar

from typing_extensions import override

from buckpass.core import IntGEZ, Policy, Submitter


class WorkerEvent(Enum):
    START = 0
    END = 1


WorkerId = TypeVar("WorkerId")
Args = TypeVar("Args")


class BurstPolicy(
    Policy[None],
    Generic[Args, WorkerId],
):
    __args: Args
    __workers_batch_size: IntGEZ
    __submitter: Submitter[WorkerId, Args]

    def __init__(
        self,
        args: Args,
        batch_size: IntGEZ,
        submitter: Submitter[WorkerId, Args],
        # TODO: max jobs sent
    ) -> None:
        super().__init__()

        self.__args = args
        self.__workers_batch_size = batch_size
        self.__submitter = submitter

        for _ in range(batch_size):
            _ = self.__submitter.submit(self.__args)

    @override
    def update(self, event: None) -> None:
        pass
