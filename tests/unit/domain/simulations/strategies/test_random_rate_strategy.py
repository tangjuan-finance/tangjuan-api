import copy
from app.domain.entities import AssetDomain
from app.domain.simulations.strategies import RandomRateStrategy
from decimal import Decimal, ROUND_HALF_UP


class TestRandomRateStrategyCase:
    @staticmethod
    def _generate_asset_simulate(asset: AssetDomain) -> dict:
        return RandomRateStrategy.apply(
            value=Decimal(asset.amount).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            min_rate=asset.min_yearly_return_rate,
            max_rate=asset.max_yearly_return_rate,
        )

    def test_check_simulate_result_boundry(self, default_asset_domain):
        # Arrange: Clone the default_asset_domain to avoid mutation
        asset_clone = copy.deepcopy(default_asset_domain)

        value = self._generate_asset_simulate(asset_clone)

        # Assert: Check if value is
        assert value is not None
        assert isinstance(value, Decimal)

        # Arrange: Get rate interval
        min_rate, max_rate = (
            asset_clone.min_yearly_return_rate,
            asset_clone.max_yearly_return_rate,
        )

        # Arange: Create min boundry
        asset_clone.max_yearly_return_rate = min_rate
        min_value = self._generate_asset_simulate(asset_clone)

        # Arange: Create max boundry
        asset_clone.min_yearly_return_rate = asset_clone.max_yearly_return_rate = (
            max_rate
        )
        max_value = self._generate_asset_simulate(asset_clone)

        assert min_value <= value <= max_value
