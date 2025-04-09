import pytest
from app.service.simulations import ScenarioAssetSimulationService
from app.domain.entities import AssetDomain
from app.domain.associations import ScenarioAssetDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from tests.factory import create_asset, create_scenario_asset
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
        start = assoc.start_age or asset.start_age
        end = assoc.end_age or asset.end_age

        return ScenarioAssetSimulationService._generate_simulation(
            amount=amount, start=start, end=end, strategy=strategy_class
        )

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

    def test_get_scenario_assets_simulation_by_id_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all assets in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Create payload for get the init result from simulate_assets_in_scenario
        payload = self._generate_scenario_asset_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Arange: Create five new assets and assocs
        NEW_ASSET_COUNT = 5
        new_assets_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the asset
            asset = create_asset(default_account)

            # Create the assoc
            create_scenario_asset(scenario_id=default_scenario.id, asset_id=asset.id)
            new_assets_list.append(asset.id)

        # Act: Get the simulations again
        update_result = ScenarioAssetSimulationService.simulate_assets_in_scenario(
            account_id=default_account.id, payload=payload
        )

        # Act: Get the updated asset ID lists in the result
        update_assets_list = [asset["asset_id"] for asset in update_result]

        # Assert: Check if all new assets in the list
        for asset in new_assets_list:
            assert asset in update_assets_list
