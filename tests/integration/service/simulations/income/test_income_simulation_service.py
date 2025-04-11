import pytest

from app.service.simulations import IncomeSimulationService
from app.domain.entities import IncomeDomain
from app.domain.simulations.strategies import RandomRateStrategy, BaseSimulateStrategy
from decimal import Decimal
from tests.factory import IncomeDomainFactory, create_fake_id
from app.repository.entities import IncomeRepo


class TestIncomeSimulationServiceCase:
    """Test cases for IncomeSimulationService."""

    def _fake_income_simulate(
        self,
        income: IncomeDomain,
        strategy_class: BaseSimulateStrategy,
    ) -> dict:
        amount, start_age, end_age = income.amount, income.start_age, income.end_age

        return strategy_class.simulate_years(
            start=start_age, end=end_age, amount=amount
        )

    def _generate_income_payload(
        self, income: IncomeDomain, strategy: str = "random_rate"
    ) -> dict:
        return {
            "income_id": income.id,
            "strategy": strategy,
        }

    def test_get_income_simulation_by_id_service_type_checking(
        self, default_account, default_income
    ):
        """Test the simulation of an income by ID is correct typed"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create payload
        payload = self._generate_income_payload(income=default_income)

        # Act: Get the simulation with default strategy
        result = IncomeSimulationService.simulate_income(
            account_id=account_id, payload=payload
        )
        ages, values = result.get("ages"), result.get("values")

        # Assert: Check if both ages and values existed
        assert ages is not None
        assert values is not None

        # Assert: Check if both ages and values are a list
        assert isinstance(ages, list)
        assert isinstance(values, list)

    def test_get_income_simulation_by_id_service_with_default_strategy(
        self, default_account, default_income
    ):
        """Test the random rate simulation of an income by ID"""
        # Arrange: Specifying strategy
        strategy = "random_rate"

        # Arrange: Get rate interval
        min_rate, max_rate = (
            default_income.min_yearly_growth_rate,
            default_income.max_yearly_growth_rate,
        )

        # Arrange: Create min boundry
        min_strategy = RandomRateStrategy(min_rate=min_rate, max_rate=min_rate)
        min_values = self._fake_income_simulate(
            income=default_income,
            strategy_class=min_strategy,
        )["values"]

        # Arrange: Create max boundry
        max_strategy = RandomRateStrategy(min_rate=max_rate, max_rate=max_rate)
        max_values = self._fake_income_simulate(
            income=default_income,
            strategy_class=max_strategy,
        )["values"]

        # Arrange: Create payload
        payload = self._generate_income_payload(
            income=default_income, strategy=strategy
        )

        # Act: Get the simulation with default strategy
        values = IncomeSimulationService.simulate_income(
            account_id=default_account.id, payload=payload
        )["values"]

        # Assert: Check if values in bound
        for idx in range(len(values)):
            assert min_values[idx] <= values[idx] <= max_values[idx]

    def test_get_income_simulation_by_id_with_invalid_strategy(
        self, default_account, default_income
    ):
        # Arrange: Set an invalid strategy
        strategy = "invalid_strategy"

        # Arrange: Create payload
        payload = self._generate_income_payload(
            income=default_income, strategy=strategy
        )

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            IncomeSimulationService.simulate_income(
                account_id=default_account.id, payload=payload
            )

    def test_get_income_simulation_by_id_service_rate_is_falsy(self, default_account):
        """Test the simulation of an income by ID when rate is falsy"""
        # Arrange: Get account id
        account_id = default_account.id

        # Arrange: Create an income with falsy rate
        income = IncomeDomainFactory(
            owner=default_account,
            min_yearly_growth_rate=Decimal("0.00"),
            max_yearly_growth_rate=Decimal("0.00"),
        )
        income_from_repo = IncomeRepo.create(income)

        # Arrange: Create payload
        payload = self._generate_income_payload(income=income_from_repo)

        # Act: Get the simulation with default strategy
        result = IncomeSimulationService.simulate_income(
            account_id=account_id, payload=payload
        )
        _, values = result.get("ages"), result.get("values")

        # Assert: Check if values existed
        assert values is not None

        # Assert: Check if the values is as expected
        for v in values:
            assert v == income.amount

    def test_get_income_simulation_by_id_service_rate_non_owner(self, default_income):
        # Arrange: Create payload
        payload = self._generate_income_payload(income=default_income)

        # Arrange: Create fake account id
        fake_account_id = create_fake_id()

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(PermissionError):
            IncomeSimulationService.simulate_income(
                account_id=fake_account_id, payload=payload
            )

    def test_get_income_simulation_by_id_service_rate_non_existed_income(
        self, default_account
    ):
        # Arrange: Create a non-saved income
        non_saved_income = IncomeDomainFactory(owner=default_account)

        # Arrange: Create payload
        payload = self._generate_income_payload(income=non_saved_income)

        # Act: Get the simulation with invalid strategy should raise Value Error
        with pytest.raises(ValueError):
            IncomeSimulationService.simulate_income(
                account_id=default_account, payload=payload
            )
