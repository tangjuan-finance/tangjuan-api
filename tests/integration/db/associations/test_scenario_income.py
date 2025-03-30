from app import db
from app.infrastructure.models import Scenario, Income, ScenarioIncome
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioIncomeModelCase:
    def test_default_scenario_income(self, default_income, default_scenario):
        # Arrange
        association = create_entity(
            ScenarioIncome,
            income=default_income,
            scenario=default_scenario,
        )
        # Act
        income_from_db = db.session.scalar(
            sa.select(Income).where(Income.id == association.income_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.scenario_id)
        )

        # Assert
        assert association.scenario_id == scenario_from_db.id
        assert association.income_id == income_from_db.id
        assert association.scenario == scenario_from_db
        assert association.income == income_from_db
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
