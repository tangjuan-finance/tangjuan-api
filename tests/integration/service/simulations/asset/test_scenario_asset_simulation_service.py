import pytest
from app.service.simulations import ScenarioAssetSimulationService
from app.domain.entities import AssetDomain
from app.domain.associations import ScenarioAssetDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from tests.factory import create_scenario_asset
from decimal import Decimal, ROUND_UP
from typing import Optional


class TestScenarioAssetSimulationServiceCase:
    """Test cases for ScenarioAssetSimulationService."""

    @pytest.fixture(scope="function")
    def default_asset_assoc(self, default_scenario, default_asset):
        yield create_scenario_asset(
            scenario_id=default_scenario.id, asset_id=default_asset.id
        )

    def _generate_scenario_asset_payload(
        self,
        scenario_id: str,
        asset_id: Optional[str] = None,
        strategy: str = "random_rate",
    ) -> dict:
        payload = {
            "scenario_id": scenario_id,
            "strategy": strategy,
        }

        if asset_id:
            payload["asset_id"] = asset_id

        return payload

    def _fake_scenario_asset_simulate(
        self,
        asset: AssetDomain,
        assoc: ScenarioAssetDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount = asset.amount
        start_age = assoc.start_age or asset.start_age
        end_age = assoc.end_age or asset.end_age

        prev = Decimal(amount).quantize(exp=Decimal("1.00"), rounding=ROUND_UP)
        values = [prev]

        for _ in range(start_age + 1, end_age + 1):
            prev = strategy_class.apply(value=prev)
            values.append(prev)

        return {
            "ages": list(range(start_age, end_age + 1)),
            "values": values,
        }

    def test_simulate_asset_in_scenario_service_type_checking(
        self, default_account, default_asset_assoc
    ):
        """Test the simulation of an asset by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_asset_assoc.scenario_id,
            asset_id=default_asset_assoc.asset_id,
        )

        # Act: Get the simulation with default strategy
        result = ScenarioAssetSimulationService.simulate_asset_in_scenario(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_scenario_asset_simulation_by_id_service_with_default_strategy(
        self, default_account, default_scenario, default_asset
    ):
        """Test the random rate simulation of an asset by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create Assoc
        assoc = create_scenario_asset(
            scenario_id=default_scenario.id, asset_id=default_asset.id
        )

        # Arrange: Get rate interval
        min_rate, max_rate = (
            assoc.min_yearly_return_rate,
            assoc.max_yearly_return_rate,
        )

        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_values = self._fake_scenario_asset_simulate(
            asset=default_asset,
            assoc=assoc,
            strategy_class=min_strategy,
        )["values"]

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_values = self._fake_scenario_asset_simulate(
            asset=default_asset,
            assoc=assoc,
            strategy_class=max_strategy,
        )["values"]

        # Arrange: Create payload
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_scenario.id,
            asset_id=default_asset.id,
            strategy=strategy,
        )

        # Act: Get the simulation with default strategy
        values = ScenarioAssetSimulationService.simulate_asset_in_scenario(
            account_id=default_account.id, payload=payload
        )["values"]
        breakpoint()
        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_scenario_asset_simulation_by_id_with_invalid_strategy(
        self, default_account, default_asset_assoc
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_asset_assoc.scenario_id,
            asset_id=default_asset_assoc.asset_id,
            strategy=strategy,
        )

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            ScenarioAssetSimulationService.simulate_asset_in_scenario(
                account_id=default_account.id, payload=payload
            )
