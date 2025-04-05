from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


class BaseSimulateStrategy(ABC):
    @classmethod
    @abstractmethod
    def apply(
        cls,
        value,
    ) -> Decimal:
        """Simulate value changes by one year"""
        pass

    def _format_result(self, value: Decimal) -> Decimal:
        """Format the result to 2 decimal places using consistent rounding."""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
