from app.domain.associations import ScenarioExpenseDomain
from tests.unit.factories import ExpenseDomainFactory
from decimal import Decimal
from datetime import datetime, timezone


class TestScenarioExpenseDomainCase:
    def test_create_scenario_expense_domain(self, default_scenario_domain):
        # Arrange
        name = "expense for scenario"

        default_max_yearly_growth_rate = Decimal("0.2")
        expense = ExpenseDomainFactory(
            name=name, max_yearly_growth_rate=default_max_yearly_growth_rate
        )
        max_yearly_growth_rate = Decimal("0.7")
        # Act
        scenario_expense = ScenarioExpenseDomain(
            expense_id=expense.id,
            scenario_id=default_scenario_domain.id,
            max_yearly_growth_rate=max_yearly_growth_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_expense.scenario_id == default_scenario_domain.id
        assert scenario_expense.expense_id == expense.id
        assert scenario_expense.max_yearly_growth_rate != default_max_yearly_growth_rate
        assert scenario_expense.max_yearly_growth_rate == max_yearly_growth_rate
