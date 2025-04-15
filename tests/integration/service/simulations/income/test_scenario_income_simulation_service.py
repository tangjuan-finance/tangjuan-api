import pytest
from app.service.simulations import ScenarioIncomeSimulationService
from app.domain.entities import IncomeDomain
from app.domain.associations import ScenarioIncomeDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from tests.factory import (
    create_income,
    create_scenario_income,
    create_fake_id,
    IncomeDomainFactory,
    ScenarioIncomeDomainFactory,
    ScenarioDomainFactory,
)
from typing import Optional
from decimal import Decimal
from collections import defaultdict


class TestScenarioIncomeSimulationServiceCase:
    """Test cases for ScenarioIncomeSimulationService."""

    @pytest.fixture(scope="function")
    def default_income_assoc(self, default_scenario, default_income):
        yield create_scenario_income(
            scenario_id=default_scenario.id, income_id=default_income.id
        )

    def _generate_scenario_income_payload(
        self,
        scenario_id: str,
        income_id: Optional[str] = None,
        strategy: str = "random_rate",
    ) -> dict:
        payload = {
            "scenario_id": scenario_id,
            "strategy": strategy,
        }

        if income_id:
            payload["income_id"] = income_id

        return payload

    @classmethod
    def _fake_scenario_income_simulate(
        cls,
        income: IncomeDomain,
        assoc: ScenarioIncomeDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount = income.amount
        start_age = assoc.start_age or income.start_age
        end_age = assoc.end_age or income.end_age

        return strategy_class.simulate_years(
            start=start_age, end=end_age, amount=amount
        )

    @classmethod
    def _create_min_max_simulations(
        cls,
        income: IncomeDomain,
        assoc: ScenarioIncomeDomain,
        min_rate: Decimal,
        max_rate: Decimal,
        strategy_class: BaseSimulateStrategy,
    ) -> tuple:
        # Arrange: Create min boundry
        min_strategy = strategy_class(min_rate=min_rate, max_rate=min_rate)
        min_simulations = cls._fake_scenario_income_simulate(
            income=income,
            assoc=assoc,
            strategy_class=min_strategy,
        )

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_simulations = cls._fake_scenario_income_simulate(
            income=income,
            assoc=assoc,
            strategy_class=max_strategy,
        )

        return min_simulations, max_simulations

    def test_simulate_income_in_scenario_service_type_checking(
        self, default_account, default_income_assoc
    ):
        """Test the simulation of an income by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=default_income_assoc.scenario_id,
            income_id=default_income_assoc.income_id,
        )

        # Act: Get the simulation with default strategy
        result = ScenarioIncomeSimulationService.simulate_income_in_scenario(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_scenario_income_simulation_by_id_service_with_default_strategy(
        self, default_account, default_scenario, default_income
    ):
        """Test the random rate simulation of an income by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create Assoc
        assoc = create_scenario_income(
            scenario_id=default_scenario.id, income_id=default_income.id
        )

        # Arrange: Generate min-max boundry
        min_simulations, max_simulations = self._create_min_max_simulations(
            income=default_income,
            assoc=assoc,
            min_rate=assoc.min_yearly_growth_rate,
            max_rate=assoc.max_yearly_growth_rate,
            strategy_class=RandomRateStrategy,
        )
        min_values, max_values = min_simulations["values"], max_simulations["values"]

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=default_scenario.id,
            income_id=default_income.id,
            strategy=strategy,
        )

        # Act: Get the simulation with default strategy
        values = ScenarioIncomeSimulationService.simulate_income_in_scenario(
            account_id=default_account.id, payload=payload
        )["values"]

        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_scenario_income_simulation_by_id_with_invalid_strategy(
        self, default_account, default_income_assoc
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=default_income_assoc.scenario_id,
            income_id=default_income_assoc.income_id,
            strategy=strategy,
        )

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.simulate_income_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_income_simulation_by_id_service_rate_non_owner(
        self, default_income_assoc
    ):
        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=default_income_assoc.scenario_id,
            income_id=default_income_assoc.income_id,
        )

        # Arrange: Create fake account id
        fake_account_id = create_fake_id()

        # Act: Get the simulation with non-owner account should raise PermissionError
        with pytest.raises(PermissionError):
            ScenarioIncomeSimulationService.simulate_income_in_scenario(
                account_id=fake_account_id, payload=payload
            )

    def test_get_scenario_income_simulation_by_id_service_rate_non_existed_income(
        self, default_account, default_scenario
    ):
        # Arrange: Create a non-saved income
        non_saved_income = IncomeDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved income without saving the association
        assoc = ScenarioIncomeDomainFactory(
            scenario_id=default_scenario.id, income_id=non_saved_income.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=assoc.scenario_id,
            income_id=assoc.income_id,
        )

        # Act: Get the simulation with non-saved income should raise ValueError
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.simulate_income_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_income_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_income
    ):
        # Arrange: Create a non-saved income
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioIncomeDomainFactory(
            scenario_id=non_saved_scenario.id, income_id=default_income.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=assoc.scenario_id,
            income_id=assoc.income_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.simulate_income_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_income_simulation_by_id_service_rate_non_existed_assoc(
        self, default_account, default_scenario, default_income
    ):
        # Arrange: Create non-saved association
        assoc = ScenarioIncomeDomainFactory(
            scenario_id=default_scenario.id, income_id=default_income.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=assoc.scenario_id,
            income_id=assoc.income_id,
        )

        # Act: Get the simulation with non-saved association should raise ValueError
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.simulate_income_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_incomes_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all incomes in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create five new incomes and assocs
        NEW_ASSET_COUNT = 5
        new_incomes_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the income
            income = create_income(owner=default_account)

            # Create the assoc
            create_scenario_income(scenario_id=default_scenario.id, income_id=income.id)
            new_incomes_list.append(income.id)

        # Arrange: Create payload for get result from simulate_incomes_in_scenario
        payload = self._generate_scenario_income_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the simulations
        update_result = ScenarioIncomeSimulationService.simulate_incomes_in_scenario(
            account_id=default_account.id, payload=payload
        )

        # Act: Get the updated income ID lists in the result
        update_incomes_list = [income["income_id"] for income in update_result]

        # Assert: Check if all new incomes in the list
        for income in new_incomes_list:
            assert income in update_incomes_list

    def test_get_scenario_incomes_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_income
    ):
        # Arrange: Create a non-saved income
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioIncomeDomainFactory(
            scenario_id=non_saved_scenario.id, income_id=default_income.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=assoc.scenario_id,
            income_id=assoc.income_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.simulate_incomes_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_aggregate_scenario_income_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all incomes in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Define the min-max boundry
        aggregrate_min_simulation = defaultdict(Decimal)
        aggregrate_max_simulation = defaultdict(Decimal)

        # Arange: Create five new incomes and assocs
        NEW_ASSET_COUNT = 5
        new_incomes_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the income
            income = create_income(owner=default_account)

            # Create the assoc
            assoc = create_scenario_income(
                scenario_id=default_scenario.id, income_id=income.id
            )
            new_incomes_list.append(income.id)

            # Create the min-max boundry
            min_simulations, max_simulations = self._create_min_max_simulations(
                income=income,
                assoc=assoc,
                min_rate=assoc.min_yearly_growth_rate,
                max_rate=assoc.max_yearly_growth_rate,
                strategy_class=RandomRateStrategy,
            )

            # Update min values to aggregate
            for age, value in zip(min_simulations["ages"], min_simulations["values"]):
                aggregrate_min_simulation[age] += value

            # Update max values to aggregate
            for age, value in zip(max_simulations["ages"], max_simulations["values"]):
                aggregrate_max_simulation[age] += value

        # Arrange: Create payload for get the result from simulate_incomes_in_scenario
        payload = self._generate_scenario_income_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the aggregate result
        aggregate_values = (
            ScenarioIncomeSimulationService.aggregate_incomes_in_scenario(
                account_id=default_account.id, payload=payload
            )
        )

        for age, value in zip(aggregate_values["ages"], aggregate_values["values"]):
            assert (
                aggregrate_min_simulation[age]
                <= value
                <= aggregrate_max_simulation[age]
            )

    def test_get_aggregate_scenario_incomes_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_income
    ):
        # Arrange: Create a non-saved income
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioIncomeDomainFactory(
            scenario_id=non_saved_scenario.id, income_id=default_income.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_income_payload(
            scenario_id=assoc.scenario_id,
            income_id=assoc.income_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioIncomeSimulationService.aggregate_incomes_in_scenario(
                account_id=default_account.id, payload=payload
            )
