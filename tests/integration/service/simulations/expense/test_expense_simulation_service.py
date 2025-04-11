import pytest

from app.service.simulations import ExpenseSimulationService
from app.domain.entities import ExpenseDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from decimal import Decimal
from tests.factory import ExpenseDomainFactory, create_fake_id
from app.repository.entities import ExpenseRepo


class TestExpenseSimulationServiceCase:
    """Test cases for ExpenseSimulationService."""

    def _fake_expense_simulate(
        self,
        expense: ExpenseDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount, start_age, end_age = expense.amount, expense.start_age, expense.end_age

        return strategy_class.simulate_years(
            start=start_age, end=end_age, amount=amount
        )

    def _generate_expense_payload(
        self, expense: ExpenseDomain, strategy: str = "random_rate"
    ) -> dict:
        return {
            "expense_id": expense.id,
            "strategy": strategy,
        }

    def test_get_expense_simulation_by_id_service_type_checking(
        self, default_account, default_expense
    ):
        """Test the simulation of an expense by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_expense_payload(expense=default_expense)

        # Act: Get the simulation with default strategy
        result = ExpenseSimulationService.simulate_expense(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_expense_simulation_by_id_service_with_default_strategy(
        self, default_account, default_expense
    ):
        """Test the random rate simulation of an expense by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_expense.min_yearly_growth_rate,
            default_expense.max_yearly_growth_rate,
        )

        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_values = self._fake_expense_simulate(
            expense=default_expense,
            strategy_class=min_strategy,
        )["values"]

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_values = self._fake_expense_simulate(
            expense=default_expense,
            strategy_class=max_strategy,
        )["values"]

        # Arrange: Create payload
        payload = self._generate_expense_payload(
            expense=default_expense, strategy=strategy
        )

        # Act: Get the simulation with default strategy
        values = ExpenseSimulationService.simulate_expense(
            account_id=default_account.id, payload=payload
        )["values"]

        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_expense_simulation_by_id_with_invalid_strategy(
        self, default_account, default_expense
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_expense_payload(
            expense=default_expense, strategy=strategy
        )

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            ExpenseSimulationService.simulate_expense(
                account_id=default_account.id, payload=payload
            )

    def test_get_expense_simulation_by_id_service_rate_is_falsy(self, default_account):
        """Test the simulation of an expense by ID when rate is falsy"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create an expense with falsy rate
        expense = ExpenseDomainFactory(
            owner=default_account,
            min_yearly_growth_rate=Decimal("0.00"),
            max_yearly_growth_rate=Decimal("0.00"),
        )
        expense_from_repo = ExpenseRepo.create(expense)

        # Arrange: Create payload
        payload = self._generate_expense_payload(expense=expense_from_repo)

        # Act: Get the simulation with default strategy
        result = ExpenseSimulationService.simulate_expense(
            account_id=account_id, payload=payload
        )
        _, values = result.get("ages"), result.get("values")

        # Assert: Check if values existed
        assert values is not None

        # Assert: Check if the values is as expected
        for v in values:
            assert v == expense.amount

    def test_get_expense_simulation_by_id_service_rate_non_owner(self, default_expense):
        # Arrange: Create payload
        payload = self._generate_expense_payload(expense=default_expense)

        # Arrange: Create fake account id
        fake_account_id = create_fake_id()

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(PermissionError):
            ExpenseSimulationService.simulate_expense(
                account_id=fake_account_id, payload=payload
            )

    def test_get_expense_simulation_by_id_service_rate_non_existed_expense(
        self, default_account
    ):
        # Arrange: Create a non-saved expense
        non_saved_expense = ExpenseDomainFactory(owner=default_account)

        # Arrange: Create payload
        payload = self._generate_expense_payload(expense=non_saved_expense)

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            ExpenseSimulationService.simulate_expense(
                account_id=default_account, payload=payload
            )
