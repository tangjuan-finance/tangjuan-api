from app import db
from app.models import Scenario, Risk, ScenarioRisk
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
            sa.select(Risk).where(Risk.id == association.right_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.left_id)
        )

        # Assert
        assert association.left_id == scenario_from_db.id
        assert association.right_id == risk_from_db.id
        assert association.scenario == scenario_from_db
        assert association.risk == risk_from_db
