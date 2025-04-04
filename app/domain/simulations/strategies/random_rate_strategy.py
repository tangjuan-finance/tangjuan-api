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
        value: int,
        start_age: int,
        end_age: int,
        min_rate: Decimal,
        max_rate: Decimal,
    ) -> dict:
        """Simulate value changes with a random rate applied yearly between min_rate and max_rate."""
        # Init value, which is the first year
        prev = Decimal(value)
        values = [prev]

        # Calculate duration
        duration = end_age - start_age

        for _ in range(duration):
            rate = cls._generate_random_rate(min_rate, max_rate)
            change_factor = Decimal("1") + rate
            simulated_value = (prev * change_factor).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            values.append(simulated_value)
            prev = simulated_value

        return {
            "ages": list(range(start_age, end_age + 1)),
            "values": values,
        }
