from tests.factory import AssetDomainFactory
from app.domain.entities import AssetDomain
from app.domain.simulations.strategies import CashAllocatedRandomRateStrategy
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


class TestCashAllocatedRandomRateStrategyCase:
    cash_flow = 10000
    allocated_rate = 0.3
    allocated_cash = Decimal(cash_flow * allocated_rate).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    @classmethod
    def _generate_asset_simulate(
        cls, asset: AssetDomain, cash: Optional[Decimal] = None
    ) -> dict:
        return CashAllocatedRandomRateStrategy.apply(
            value=Decimal(asset.amount).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
            cash=cash or cls.allocated_cash,  # cls.allocated_cash as default
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

    def test_check_simulate_cash_flow_addup(self):
        # Arrange: Create a fresh asset as this test would alter asset domain
        asset = AssetDomainFactory()

        # Arange: Create fix rate asset
        asset.max_yearly_return_rate = asset.min_yearly_return_rate
        fixed_rate_value_with_cash = self._generate_asset_simulate(asset)

        # Arange: Create fix rate asset without cash
        less_cash = Decimal("1000")
        fixed_rate_value_without_cash = self._generate_asset_simulate(
            asset, cash=less_cash
        )

        # Arrange: Get difference between with and without cash
        diff = self.allocated_cash - less_cash

        assert fixed_rate_value_without_cash < fixed_rate_value_with_cash
        assert fixed_rate_value_without_cash + diff == fixed_rate_value_with_cash
