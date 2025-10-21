from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar


class IntGEZ(int):
    """int >= 0."""

    def __new__(cls, value: int) -> Self:
        assert value >= 0
        return super().__new__(cls, value)


class IntGTZ(int):
    """int > 0."""

    def __new__(cls, value: int) -> Self:
        assert value > 0
        return super().__new__(cls, value)


Event = TypeVar("Event")


class Policy(ABC, Generic[Event]):
    @abstractmethod
    def update(self, event: Event) -> None:
        pass


JobId = TypeVar("JobId")
Args = TypeVar("Args")


class Submitter(ABC, Generic[JobId, Args]):
    @abstractmethod
    def submit(self, args: Args) -> JobId:
        pass
