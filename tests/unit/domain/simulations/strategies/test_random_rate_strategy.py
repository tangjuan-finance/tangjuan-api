from tests.factory import AssetDomainFactory
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

    def test_check_simulate_result_boundry(self):
        # Arrange: Create a fresh asset as this test would alter asset domain
        asset = AssetDomainFactory()

        value = self._generate_asset_simulate(asset)

        # Assert: Check if value is
        assert value is not None
        assert isinstance(value, Decimal)

        # Arrange: Get rate interval
        min_rate, max_rate = (
            asset.min_yearly_return_rate,
            asset.max_yearly_return_rate,
        )

        # Arange: Create min boundry
        asset.max_yearly_return_rate = min_rate
        min_value = self._generate_asset_simulate(asset)

        # Arange: Create max boundry
        asset.min_yearly_return_rate = asset.max_yearly_return_rate = max_rate
        max_value = self._generate_asset_simulate(asset)

        assert min_value <= value <= max_value
