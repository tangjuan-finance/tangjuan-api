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

    @staticmethod
    def _valid_input(
        value: int,
        start_age: int,
        end_age: int,
        min_rate: Decimal,
        max_rate: Decimal,
    ) -> str:
        if not isinstance(value, int):
            raise ValueError(
                f"value should be int, gave {type(value).__name__} instead"
            )
        if not isinstance(start_age, int):
            raise ValueError(
                f"start_age should be int, gave {type(start_age).__name__} instead"
            )
        if not isinstance(end_age, int):
            raise ValueError(
                f"end_age should be int, gave {type(end_age).__name__} instead"
            )
        if not isinstance(min_rate, Decimal):
            raise ValueError(
                f"min_rate should be Decimal, gave {type(min_rate).__name__} instead"
            )
        if not isinstance(max_rate, Decimal):
            raise ValueError(
                f"max_rate should be Decimal, gave {type(max_rate).__name__} instead"
            )
        if start_age > end_age:
            raise ValueError(
                f"start_age should larger than end_age, but start_age({start_age}) is less than end_age({end_age})"
            )
        if min_rate > max_rate:
            raise ValueError(
                f"min_rate should larger than max_rate, but min_rate({min_rate}) is less than max_rate({max_rate})"
            )

        return "Input validated."

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
        # Valid Input
        cls._valid_input(
            value=value,
            start_age=start_age,
            end_age=end_age,
            min_rate=min_rate,
            max_rate=max_rate,
        )

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
