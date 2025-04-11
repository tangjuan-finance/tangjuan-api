from app.domain.entities import AssetDomain
from app.domain.simulations.strategies import RandomRateStrategy
from decimal import Decimal, ROUND_HALF_UP


class TestRandomRateStrategyCase:
    @classmethod
    def _create_strategy(cls, asset: AssetDomain) -> RandomRateStrategy:
        min_rate = asset.min_yearly_return_rate
        max_rate = asset.max_yearly_return_rate

        return RandomRateStrategy(min_rate=min_rate, max_rate=max_rate)

    @classmethod
    def _simulate_asset(cls, amount: int, strategy: RandomRateStrategy) -> dict:
        return strategy.apply(
            value=Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        )

    def test_check_simulate_year_boundry(self, default_asset_domain):
        # Arrange: Get amount
        amount, start, end = (
            default_asset_domain.amount,
            default_asset_domain.start_age,
            default_asset_domain.end_age,
        )

        # Arrange: Get min-max rate
        min_rate, max_rate = (
            default_asset_domain.min_yearly_return_rate,
            default_asset_domain.max_yearly_return_rate,
        )

        # Arrange: Get min-max boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_values = min_strategy.simulate_years(start=start, end=end, amount=amount)[
            "values"
        ]

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_values = max_strategy.simulate_years(start=start, end=end, amount=amount)[
            "values"
        ]

        # Act: Create strategy
        strategy = self._create_strategy(default_asset_domain)

        # Act: Create simulate by year ranges
        values = strategy.simulate_years(start=start, end=end, amount=amount)["values"]

        if not values:
            raise ValueError(f"Values simulated from strategy {strategy} missing")

        # Assert: Check if values in max-min boundry
        for idx in range(len(values)):
            min_values[idx] <= values[idx] <= max_values[idx]
