import pytest
from app.service.simulations import AssetSimulationService
from app.domain.entities import AssetDomain
from tests.factory import create_asset
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from decimal import Decimal, ROUND_UP


class TestAssetSimulationServiceCase:
    """Test cases for AssetSimulationService."""

    def _fake_asset_simulate(
        self,
        value: Decimal,
        min_rate: Decimal,
        max_rate: Decimal,
        start_age: int,
        end_age: int,
        Strategy: BaseSimulateStrategy,
        **kwargs,
    ) -> dict:
        prev = Decimal(value).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start_age + 1, end_age + 1):
            prev = Strategy.apply(
                value=prev, min_rate=min_rate, max_rate=max_rate, **kwargs
            )
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
        self, default_account
    ):
        """Test the random rate simulation of an asset by ID"""
        # Arrange: Create a fresh asset by repo as this test would alter asset domain
        asset = create_asset(owner=default_account)

        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_asset_payload(asset=asset, strategy=strategy)

        # Act: Get the simulation with default strategy
        values = AssetSimulationService.simulate_asset(
            account_id=account_id, payload=payload
        )["values"]

        # Arrange: Create bound
        value = asset.amount
        min_rate, max_rate = asset.min_yearly_return_rate, asset.max_yearly_return_rate
        start_age, end_age = asset.start_age, asset.end_age
        min_values = self._fake_asset_simulate(
            value=value,
            min_rate=min_rate,
            max_rate=min_rate,
            start_age=start_age,
            end_age=end_age,
            Strategy=RandomRateStrategy,
        )["values"]
        max_values = self._fake_asset_simulate(
            value=value,
            min_rate=max_rate,
            max_rate=max_rate,
            start_age=start_age,
            end_age=end_age,
            Strategy=RandomRateStrategy,
        )["values"]

        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_asset_simulation_by_id_with_invalid_strategy(
        self, default_account, default_asset
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_asset_payload(asset=default_asset, strategy=strategy)

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            AssetSimulationService.simulate_asset(
                account_id=account_id, payload=payload
            )
