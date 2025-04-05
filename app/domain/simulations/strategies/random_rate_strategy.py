from .base import BaseSimulateStrategy
from decimal import Decimal
import random


class RandomRateStrategy(BaseSimulateStrategy):
    @staticmethod
    def _generate_random_rate(min_rate: Decimal, max_rate: Decimal) -> Decimal:
        """Generate a random Decimal rate between min_rate and max_rate, rounded to 2 decimals."""

        # Convert to float for random.uniform, then back to Decimal
        random_float = random.uniform(float(min_rate), float(max_rate))
        return Decimal(str(round(random_float, 2)))

    @classmethod
    def calculate_next(
        cls,
        prev: Decimal,
        min_rate: Decimal,
        max_rate: Decimal,
    ) -> Decimal:
        """Calculate next value."""
        rate = cls._generate_random_rate(min_rate, max_rate)
        return prev * (Decimal("1") + rate)
