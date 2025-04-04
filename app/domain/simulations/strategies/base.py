from abc import ABC, abstractmethod


class BaseSimulateStrategy(ABC):
    @classmethod
    @abstractmethod
    def apply(cls, value: int, start_age: int, end_age: int, *args, **kwargs):
        pass
