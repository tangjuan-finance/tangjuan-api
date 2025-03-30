from app import db
from app.infrastructure.models import Scenario, Child, ScenarioChild
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioChildModelCase:
    def test_default_scenario_child(self, default_child, default_scenario):
        # Arrange
        association = create_entity(
            ScenarioChild,
            child=default_child,
            scenario=default_scenario,
        )
        # Act
        child_from_db = db.session.scalar(
            sa.select(Child).where(Child.id == association.child_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.scenario_id)
        )

        # Assert
        assert association.scenario_id == scenario_from_db.id
        assert association.child_id == child_from_db.id
        assert association.scenario == scenario_from_db
        assert association.child == child_from_db
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
