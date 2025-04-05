from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


class BaseSimulateStrategy(ABC):
    @classmethod
    @abstractmethod
    def calculate_next(
        cls,
        prev,
        **kwargs,
    ):
        """Calculate next should be implement at subclass"""
        pass

    @classmethod
    def apply(
        cls,
        value: int,
        start_age: int,
        end_age: int,
        **kwargs,
    ) -> dict:
        """Simulate value changes with between min_rate and max_rate."""
        # Init value, which is the first year
        prev = Decimal(value)
        values = [prev]
        duration = end_age - start_age

        for _ in range(duration):
            updated = cls.calculate_next(prev=prev, **kwargs)
            updated = updated.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            values.append(updated)
            prev = updated

        return {
            "ages": list(range(start_age, end_age + 1)),
            "values": values,
        }
