from app import db
from app.infrastructure.models import Scenario, Risk, ScenarioRisk
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioRiskModelCase:
    def test_default_scenario_risk(self, default_risk, default_scenario):
        # Arrange
        association = create_entity(
            ScenarioRisk,
            risk=default_risk,
            scenario=default_scenario,
        )
        # Act
        risk_from_db = db.session.scalar(
            sa.select(Risk).where(Risk.id == association.risk_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.scenario_id)
        )

        # Assert
        assert association.scenario_id == scenario_from_db.id
        assert association.risk_id == risk_from_db.id
        assert association.scenario == scenario_from_db
        assert association.risk == risk_from_db
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
