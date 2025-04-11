from dataclasses import dataclass
from .base import BaseSimulateStrategy
from .mixin import YearlyValueSimulationMixin
from decimal import Decimal
import random


@dataclass
class RandomRateStrategy(BaseSimulateStrategy, YearlyValueSimulationMixin):
    min_rate: Decimal
    max_rate: Decimal

    def _generate_random_rate(self) -> Decimal:
        """
        Generate a random rate between min_rate and max_rate as a Decimal,
        rounded to 2 decimal places.
        """
        # Convert to float for random.uniform, then back to Decimal
        random_float = random.uniform(float(self.min_rate), float(self.max_rate))
        return Decimal(str(round(random_float, 2)))

    def apply(
        self,
        value: Decimal,
    ) -> Decimal:
        """Calculate next value by applying a random rate."""
        rate = self._generate_random_rate()
        result = value * (Decimal("1") + rate)
        # Calculate the new value and round it to 2 decimal places
        return self._format_result(result)

    def simulate_years(self, start: int, end: int, amount: int) -> list:
        return self._format_output(
            ages=self._get_duration(start=start, end=end),
            values=self._simulate_years(start=start, end=end, amount=amount),
        )
