import pytest
from app.service.simulations import ScenarioAssetSimulationService
from app.domain.entities import AssetDomain
from app.domain.associations import ScenarioAssetDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from tests.factory import create_asset, create_scenario_asset
from typing import Optional
from decimal import Decimal
from collections import defaultdict


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

    @classmethod
    def _fake_scenario_asset_simulate(
        cls,
        asset: AssetDomain,
        assoc: ScenarioAssetDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount = asset.amount
        start = assoc.start_age or asset.start_age
        end = assoc.end_age or asset.end_age

        return ScenarioAssetSimulationService._generate_simulation(
            amount=amount, start=start, end=end, strategy=strategy_class
        )

    @classmethod
    def _create_min_max_simulations(
        cls,
        asset: AssetDomain,
        assoc: ScenarioAssetDomain,
        min_rate: Decimal,
        max_rate: Decimal,
        strategy_class: BaseSimulateStrategy,
    ) -> tuple:
        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_simulations = cls._fake_scenario_asset_simulate(
            asset=asset,
            assoc=assoc,
            strategy_class=min_strategy,
        )

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_simulations = cls._fake_scenario_asset_simulate(
            asset=asset,
            assoc=assoc,
            strategy_class=max_strategy,
        )

        return min_simulations, max_simulations

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

        # Arrange: Generate min-max boundry
        min_simulations, max_simulations = self._create_min_max_simulations(
            asset=default_asset,
            assoc=assoc,
            min_rate=assoc.min_yearly_return_rate,
            max_rate=assoc.max_yearly_return_rate,
            strategy_class=RandomRateStrategy,
        )
        min_values, max_values = min_simulations["values"], max_simulations["values"]

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

    def test_get_scenario_assets_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all assets in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create five new assets and assocs
        NEW_ASSET_COUNT = 5
        new_assets_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the asset
            asset = create_asset(default_account)

            # Create the assoc
            create_scenario_asset(scenario_id=default_scenario.id, asset_id=asset.id)
            new_assets_list.append(asset.id)

        # Arrange: Create payload for get result from simulate_assets_in_scenario
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the simulations
        update_result = ScenarioAssetSimulationService.simulate_assets_in_scenario(
            account_id=default_account.id, payload=payload
        )

        # Act: Get the updated asset ID lists in the result
        update_assets_list = [asset["asset_id"] for asset in update_result]

        # Assert: Check if all new assets in the list
        for asset in new_assets_list:
            assert asset in update_assets_list

    def test_get_aggregate_scenario_asset_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all assets in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Define the min-max boundry
        aggregrate_min_simulation = defaultdict(Decimal)
        aggregrate_max_simulation = defaultdict(Decimal)

        # Arange: Create five new assets and assocs
        NEW_ASSET_COUNT = 5
        new_assets_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the asset
            asset = create_asset(default_account)

            # Create the assoc
            assoc = create_scenario_asset(
                scenario_id=default_scenario.id, asset_id=asset.id
            )
            new_assets_list.append(asset.id)

            # Create the min-max boundry
            min_simulations, max_simulations = self._create_min_max_simulations(
                asset=asset,
                assoc=assoc,
                min_rate=assoc.min_yearly_return_rate,
                max_rate=assoc.max_yearly_return_rate,
                strategy_class=RandomRateStrategy,
            )

            # Update min values to aggregate
            for age, value in zip(min_simulations["ages"], min_simulations["values"]):
                aggregrate_min_simulation[age] += value

            # Update max values to aggregate
            for age, value in zip(max_simulations["ages"], max_simulations["values"]):
                aggregrate_max_simulation[age] += value

        # Arrange: Create payload for get the result from simulate_assets_in_scenario
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the aggregate result
        aggregate_values = ScenarioAssetSimulationService.aggregate_assets_in_scenario(
            account_id=default_account.id, payload=payload
        )

        for age, value in zip(aggregate_values["ages"], aggregate_values["values"]):
            assert (
                aggregrate_min_simulation[age]
                <= value
                <= aggregrate_max_simulation[age]
            )
