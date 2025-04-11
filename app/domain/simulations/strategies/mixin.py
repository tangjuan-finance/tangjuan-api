from decimal import Decimal, ROUND_UP


class YearlyValueSimulationMixin:
    def _simulate_years(self, start: int, end: int, amount: int) -> list:
        """
        Simulate value growth over a given period using a simulation strategy.
        """
        prev = Decimal(amount).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start + 1, end + 1):
            prev = self.apply(prev)
            values.append(prev)
        return values
