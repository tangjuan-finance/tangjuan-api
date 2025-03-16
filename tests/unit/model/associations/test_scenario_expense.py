from app import db
from app.models import Scenario, Expense, ScenarioExpense
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioExpenseModelCase:
    def test_default_scenario_expense(self, default_expense, default_scenario):
        # Arrange
        association = create_entity(
            ScenarioExpense,
            expense=default_expense,
            scenario=default_scenario,
        )
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.id == association.right_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.left_id)
        )

        # Assert
        assert association.left_id == scenario_from_db.id
        assert association.right_id == expense_from_db.id
        assert association.scenario == scenario_from_db
        assert association.expense == expense_from_db
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
