from .base import BaseSimulateStrategy
from decimal import Decimal, ROUND_HALF_UP
import random


class RandomRateStrategy(BaseSimulateStrategy):
    @staticmethod
    def _generate_random_rate(min_rate: Decimal, max_rate: Decimal) -> Decimal:
        """Generate a random Decimal rate between min_rate and max_rate, rounded to 2 decimals."""

        # Convert to float for random.uniform, then back to Decimal
        random_float = random.uniform(float(min_rate), float(max_rate))
        return Decimal(str(round(random_float, 2)))

    @classmethod
    def apply(
        cls,
        value: Decimal,
        min_rate: Decimal,
        max_rate: Decimal,
    ) -> Decimal:
        """Calculate next value by applying a random rate."""
        rate = cls._generate_random_rate(min_rate, max_rate)

        # Calculate the new value and round it to 2 decimal places
        return (value * (Decimal("1") + rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
