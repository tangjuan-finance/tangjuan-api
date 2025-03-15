from app import db
from app.models import Scenario, Liability, ScenarioLiability
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioLiabilityModelCase:
    def test_default_scenario_liability(self, default_liability, default_scenario):
        # Arrange

        allocation_percentage = 0.6

        association = create_entity(
            ScenarioLiability,
            liability=default_liability,
            scenario=default_scenario,
            allocation_percentage=allocation_percentage,
        )
        # Act
        liability_from_db = db.session.scalar(
            sa.select(Liability).where(Liability.id == association.right_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.left_id)
        )

        # Assert
        assert association.left_id == scenario_from_db.id
        assert association.right_id == liability_from_db.id
        assert association.scenario == scenario_from_db
        assert association.liability == liability_from_db
        assert association.allocation_percentage == allocation_percentage
