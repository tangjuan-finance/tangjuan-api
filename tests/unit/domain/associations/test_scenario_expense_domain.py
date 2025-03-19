from app.domain.association import ScenarioExpenseDomain
from tests.unit.factories import ExpenseDomainFactory
from decimal import Decimal


class TestScenarioExpenseDomainCase:
    def test_create_scenario_expense_domain():
        # Arrange
        default_max_yearly_growth_rate = Decimal("0.2")
        expense = ExpenseDomainFactory(
            name="expense", max_yearly_growth_rate=default_max_yearly_growth_rate
        )
        max_yearly_growth_rate = Decimal("0.7")
        # Act
        scenario_expense = ScenarioExpenseDomain(
            expense=expense,
            max_yearly_growth_rate=max_yearly_growth_rate,
        )
        # Assert
        assert scenario_expense.expense.name == "expense"
        assert scenario_expense.max_yearly_growth_rate != default_max_yearly_growth_rate
        assert scenario_expense.max_yearly_growth_rate == max_yearly_growth_rate
