from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class IntGEZ(int):
    """Int with value x >= 0."""

    def __new__(cls, value: int) -> "IntGEZ":
        assert value >= 0
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
