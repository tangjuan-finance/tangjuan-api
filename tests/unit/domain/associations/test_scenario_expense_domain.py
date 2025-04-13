from app.domain.associations import ScenarioExpenseDomain
from tests.factory import create_fake_id
from decimal import Decimal
from datetime import datetime, timezone


class TestScenarioExpenseDomainCase:
    def test_create_scenario_expense_domain(self):
        # Arrange
        scenario_id = create_fake_id()
        expense_id = create_fake_id()
        max_yearly_growth_rate = Decimal("0.7")
        # Act
        scenario_expense = ScenarioExpenseDomain(
            expense_id=expense_id,
            scenario_id=scenario_id,
            max_yearly_growth_rate=max_yearly_growth_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_expense.scenario_id == scenario_id
        assert scenario_expense.expense_id == expense_id
        assert scenario_expense.max_yearly_growth_rate == max_yearly_growth_rate
