# from app.domain.entities import ExpenseDomain
from decimal import Decimal
from tests.unit.factories import ExpenseDomainFactory


class TestExpenseDomainCase:
    def test_create_expense_domain(
        self, default_expense_domain, default_account_domain
    ):
        # Assert
        assert default_expense_domain.name == "Default Expense Domain"
        assert default_expense_domain.amount == 50000
        assert default_expense_domain.max_yearly_growth_rate == Decimal("0.5")
        assert default_expense_domain.min_yearly_growth_rate == Decimal("-0.5")
        assert default_expense_domain.start_age == 20
        assert default_expense_domain.owner == default_account_domain

    def test_factory_expense_domain(self):
        # Arrange
        name = "Default Expense Domain"
        amount = 50000
        max_yearly_growth_rate = Decimal("0.5")
        min_yearly_growth_rate = Decimal("-0.5")
        start_age = 20

        # Act
        expense = ExpenseDomainFactory(
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
        )

        # Assert
        assert expense.name == name
        assert expense.amount == amount
        assert expense.max_yearly_growth_rate == max_yearly_growth_rate
        assert expense.min_yearly_growth_rate == min_yearly_growth_rate
        assert expense.start_age == start_age
