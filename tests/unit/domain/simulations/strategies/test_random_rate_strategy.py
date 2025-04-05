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

    def test_check_simulate_result_boundry(self, default_asset_domain):
        amount = default_asset_domain.amount

        # Arrange: Generate simulation
        strategy = self._create_strategy(asset=default_asset_domain)
        value = self._simulate_asset(amount=amount, strategy=strategy)

        # Assert: Check if value is
        assert value is not None
        assert isinstance(value, Decimal)

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_asset_domain.min_yearly_return_rate,
            default_asset_domain.max_yearly_return_rate,
        )

        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_value = self._simulate_asset(amount=amount, strategy=min_strategy)

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_value = self._simulate_asset(amount=amount, strategy=max_strategy)

        assert min_value <= value <= max_value
