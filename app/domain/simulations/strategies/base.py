from abc import ABC, abstractmethod
from decimal import Decimal


class BaseSimulateStrategy(ABC):
    @classmethod
    @abstractmethod
    def apply(
        cls,
        value,
        **kwargs,
    ) -> Decimal:
        """Simulate value changes by one year"""
        pass
