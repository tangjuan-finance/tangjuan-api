from .random_rate_strategy import RandomRateStrategy
from decimal import Decimal, ROUND_HALF_UP


class CashAllocatedRandomRateStrategy(RandomRateStrategy):
    @classmethod
    def apply(
        cls,
        value: Decimal,
        cash: Decimal,
        min_rate: Decimal,
        max_rate: Decimal,
    ) -> Decimal:
        """Calculate next value by applying a random rate and add the given cash."""
        rate = cls._generate_random_rate(min_rate, max_rate)

        # Calculate the new value and round it to 2 decimal places
        return (value * (Decimal("1") + rate) + cash).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
