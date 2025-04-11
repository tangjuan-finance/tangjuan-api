from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from .utils import format_simulation_output


class BaseSimulateStrategy(ABC):
    @abstractmethod
    def apply(
        self,
        value,
    ) -> Decimal:
        """Simulate value changes by one year"""
        pass

    @abstractmethod
    def simulate_years(self, start: int, end: int, *args, **kargs):
        pass

    def _format_result(self, value: Decimal) -> Decimal:
        """Format the result to 2 decimal places using consistent rounding."""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _get_duration(self, start: int, end: int) -> list:
        """
        Generate a list of years from start to end (inclusive).
        """
        return list(range(start, end + 1))

    def _format_output(self, ages: list, values: list) -> dict:
        """
        Format output
        """
        return format_simulation_output(ages=ages, values=values)
