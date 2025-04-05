import pytest
from app.service.simulations import AssetSimulationService
from app.domain.entities import AssetDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from decimal import Decimal, ROUND_UP


class TestAssetSimulationServiceCase:
    """Test cases for AssetSimulationService."""

    def _fake_asset_simulate(
        self,
        asset: AssetDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount, start_age, end_age = asset.amount, asset.start_age, asset.end_age

        prev = Decimal(amount).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start_age + 1, end_age + 1):
            prev = strategy_class.apply(value=prev)
            values.append(prev)

        return {
            "ages": list(range(start_age, end_age + 1)),
            "values": values,
        }

    def _generate_asset_payload(
        self, asset: AssetDomain, strategy: str = "random_rate"
    ) -> dict:
        return {
            "asset_id": asset.id,
            "strategy": strategy,
        }

    def test_get_asset_simulation_by_id_service_type_checking(
        self, default_account, default_asset
    ):
        """Test the simulation of an asset by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_asset_payload(asset=default_asset)

        # Act: Get the simulation with default strategy
        result = AssetSimulationService.simulate_asset(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_asset_simulation_by_id_service_with_default_strategy(
        self, default_account, default_asset
    ):
        """Test the random rate simulation of an asset by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_asset.min_yearly_return_rate,
            default_asset.max_yearly_return_rate,
        )

        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_values = self._fake_asset_simulate(
            asset=default_asset,
            strategy_class=min_strategy,
        )["values"]

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_values = self._fake_asset_simulate(
            asset=default_asset,
            strategy_class=max_strategy,
        )["values"]

        # Arrange: Create payload
        payload = self._generate_asset_payload(asset=default_asset, strategy=strategy)

        # Act: Get the simulation with default strategy
        values = AssetSimulationService.simulate_asset(
            account_id=default_account.id, payload=payload
        )["values"]

        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_asset_simulation_by_id_with_invalid_strategy(
        self, default_account, default_asset
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_asset_payload(asset=default_asset, strategy=strategy)

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            AssetSimulationService.simulate_asset(
                account_id=default_account.id, payload=payload
            )
