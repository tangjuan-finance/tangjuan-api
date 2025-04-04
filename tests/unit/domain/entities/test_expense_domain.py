# from app.domain.entities import ExpenseDomain
from decimal import Decimal
from tests.factory import ExpenseDomainFactory


class TestExpenseDomainCase:
    def test_factory_expense_domain(self):
        # Arrange
        name = "Default Expense Domain"
        amount = 50000
        max_yearly_growth_rate = Decimal("0.5")
        min_yearly_growth_rate = Decimal("-0.5")
        start_age = 20
        end_age = 100

        # Act
        expense = ExpenseDomainFactory(
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert expense.name == name
        assert expense.amount == amount
        assert expense.max_yearly_growth_rate == max_yearly_growth_rate
        assert expense.min_yearly_growth_rate == min_yearly_growth_rate
        assert expense.start_age == start_age
