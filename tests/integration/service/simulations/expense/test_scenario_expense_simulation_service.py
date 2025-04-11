import pytest
from app.service.simulations import ScenarioExpenseSimulationService
from app.domain.entities import ExpenseDomain
from app.domain.associations import ScenarioExpenseDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from tests.factory import (
    create_expense,
    create_scenario_expense,
    create_fake_id,
    ExpenseDomainFactory,
    ScenarioExpenseDomainFactory,
    ScenarioDomainFactory,
)
from typing import Optional
from decimal import Decimal
from collections import defaultdict


class TestScenarioExpenseSimulationServiceCase:
    """Test cases for ScenarioExpenseSimulationService."""

    @pytest.fixture(scope="function")
    def default_expense_assoc(self, default_scenario, default_expense):
        yield create_scenario_expense(
            scenario_id=default_scenario.id, expense_id=default_expense.id
        )

    def _generate_scenario_expense_payload(
        self,
        scenario_id: str,
        expense_id: Optional[str] = None,
        strategy: str = "random_rate",
    ) -> dict:
        payload = {
            "scenario_id": scenario_id,
            "strategy": strategy,
        }

        if expense_id:
            payload["expense_id"] = expense_id

        return payload

    @classmethod
    def _fake_scenario_expense_simulate(
        cls,
        expense: ExpenseDomain,
        assoc: ScenarioExpenseDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount = expense.amount
        start_age = assoc.start_age or expense.start_age
        end_age = assoc.end_age or expense.end_age

        return strategy_class.simulate_years(
            start=start_age, end=end_age, amount=amount
        )

    @classmethod
    def _create_min_max_simulations(
        cls,
        expense: ExpenseDomain,
        assoc: ScenarioExpenseDomain,
        min_rate: Decimal,
        max_rate: Decimal,
        strategy_class: BaseSimulateStrategy,
    ) -> tuple:
        # Arrange: Create min boundry
        min_strategy = strategy_class(min_rate=min_rate, max_rate=min_rate)
        min_simulations = cls._fake_scenario_expense_simulate(
            expense=expense,
            assoc=assoc,
            strategy_class=min_strategy,
        )

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_simulations = cls._fake_scenario_expense_simulate(
            expense=expense,
            assoc=assoc,
            strategy_class=max_strategy,
        )

        return min_simulations, max_simulations

    def test_simulate_expense_in_scenario_service_type_checking(
        self, default_account, default_expense_assoc
    ):
        """Test the simulation of an expense by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_expense_assoc.scenario_id,
            expense_id=default_expense_assoc.expense_id,
        )

        # Act: Get the simulation with default strategy
        result = ScenarioExpenseSimulationService.simulate_expense_in_scenario(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_scenario_expense_simulation_by_id_service_with_default_strategy(
        self, default_account, default_scenario, default_expense
    ):
        """Test the random rate simulation of an expense by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create Assoc
        assoc = create_scenario_expense(
            scenario_id=default_scenario.id, expense_id=default_expense.id
        )

        # Arrange: Generate min-max boundry
        min_simulations, max_simulations = self._create_min_max_simulations(
            expense=default_expense,
            assoc=assoc,
            min_rate=assoc.min_yearly_growth_rate,
            max_rate=assoc.max_yearly_growth_rate,
            strategy_class=RandomRateStrategy,
        )
        min_values, max_values = min_simulations["values"], max_simulations["values"]

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_scenario.id,
            expense_id=default_expense.id,
            strategy=strategy,
        )

        # Act: Get the simulation with default strategy
        values = ScenarioExpenseSimulationService.simulate_expense_in_scenario(
            account_id=default_account.id, payload=payload
        )["values"]

        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_scenario_expense_simulation_by_id_with_invalid_strategy(
        self, default_account, default_expense_assoc
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_expense_assoc.scenario_id,
            expense_id=default_expense_assoc.expense_id,
            strategy=strategy,
        )

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.simulate_expense_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_expense_simulation_by_id_service_rate_non_owner(
        self, default_expense_assoc
    ):
        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_expense_assoc.scenario_id,
            expense_id=default_expense_assoc.expense_id,
        )

        # Arrange: Create fake account id
        fake_account_id = create_fake_id()

        # Act: Get the simulation with non-owner account should raise PermissionError
        with pytest.raises(PermissionError):
            ScenarioExpenseSimulationService.simulate_expense_in_scenario(
                account_id=fake_account_id, payload=payload
            )

    def test_get_scenario_expense_simulation_by_id_service_rate_non_existed_expense(
        self, default_account, default_scenario
    ):
        # Arrange: Create a non-saved expense
        non_saved_expense = ExpenseDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved expense without saving the association
        assoc = ScenarioExpenseDomainFactory(
            scenario_id=default_scenario.id, expense_id=non_saved_expense.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=assoc.scenario_id,
            expense_id=assoc.expense_id,
        )

        # Act: Get the simulation with non-saved expense should raise ValueError
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.simulate_expense_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_expense_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_expense
    ):
        # Arrange: Create a non-saved expense
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioExpenseDomainFactory(
            scenario_id=non_saved_scenario.id, expense_id=default_expense.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=assoc.scenario_id,
            expense_id=assoc.expense_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.simulate_expense_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_expense_simulation_by_id_service_rate_non_existed_assoc(
        self, default_account, default_scenario, default_expense
    ):
        # Arrange: Create non-saved association
        assoc = ScenarioExpenseDomainFactory(
            scenario_id=default_scenario.id, expense_id=default_expense.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=assoc.scenario_id,
            expense_id=assoc.expense_id,
        )

        # Act: Get the simulation with non-saved association should raise ValueError
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.simulate_expense_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_scenario_expenses_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all expenses in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arange: Create five new expenses and assocs
        NEW_ASSET_COUNT = 5
        new_expenses_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the expense
            expense = create_expense(default_account)

            # Create the assoc
            create_scenario_expense(
                scenario_id=default_scenario.id, expense_id=expense.id
            )
            new_expenses_list.append(expense.id)

        # Arrange: Create payload for get result from simulate_expenses_in_scenario
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the simulations
        update_result = ScenarioExpenseSimulationService.simulate_expenses_in_scenario(
            account_id=default_account.id, payload=payload
        )

        # Act: Get the updated expense ID lists in the result
        update_expenses_list = [expense["expense_id"] for expense in update_result]

        # Assert: Check if all new expenses in the list
        for expense in new_expenses_list:
            assert expense in update_expenses_list

    def test_get_scenario_expenses_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_expense
    ):
        # Arrange: Create a non-saved expense
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioExpenseDomainFactory(
            scenario_id=non_saved_scenario.id, expense_id=default_expense.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=assoc.scenario_id,
            expense_id=assoc.expense_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.simulate_expenses_in_scenario(
                account_id=default_account.id, payload=payload
            )

    def test_get_aggregate_scenario_expense_simulation_service_with_default_strategy(
        self, default_account, default_scenario
    ):
        """Test the random rate simulation of all expenses in the scenario given its ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Define the min-max boundry
        aggregrate_min_simulation = defaultdict(Decimal)
        aggregrate_max_simulation = defaultdict(Decimal)

        # Arange: Create five new expenses and assocs
        NEW_ASSET_COUNT = 5
        new_expenses_list = []
        for _ in range(NEW_ASSET_COUNT):
            # Create the expense
            expense = create_expense(default_account)

            # Create the assoc
            assoc = create_scenario_expense(
                scenario_id=default_scenario.id, expense_id=expense.id
            )
            new_expenses_list.append(expense.id)

            # Create the min-max boundry
            min_simulations, max_simulations = self._create_min_max_simulations(
                expense=expense,
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

        # Arrange: Create payload for get the result from simulate_expenses_in_scenario
        payload = self._generate_scenario_expense_payload(
            scenario_id=default_scenario.id,
            strategy=strategy,
        )

        # Act: Get the aggregate result
        aggregate_values = (
            ScenarioExpenseSimulationService.aggregate_expenses_in_scenario(
                account_id=default_account.id, payload=payload
            )
        )

        for age, value in zip(aggregate_values["ages"], aggregate_values["values"]):
            assert (
                aggregrate_min_simulation[age]
                <= value
                <= aggregrate_max_simulation[age]
            )

    def test_get_aggregate_scenario_expenses_simulation_by_id_service_rate_non_existed_scenario(
        self, default_account, default_expense
    ):
        # Arrange: Create a non-saved expense
        non_saved_scenario = ScenarioDomainFactory(owner=default_account)

        # Arrange: Create association from the non-saved scenario without saving the association
        assoc = ScenarioExpenseDomainFactory(
            scenario_id=non_saved_scenario.id, expense_id=default_expense.id
        )

        # Arrange: Create payload
        payload = self._generate_scenario_expense_payload(
            scenario_id=assoc.scenario_id,
            expense_id=assoc.expense_id,
        )

        # Act: Get the simulation with non-saved scenario should raise ValueError
        with pytest.raises(ValueError):
            ScenarioExpenseSimulationService.aggregate_expenses_in_scenario(
                account_id=default_account.id, payload=payload
            )
