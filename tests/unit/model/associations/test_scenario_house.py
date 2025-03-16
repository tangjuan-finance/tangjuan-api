from app import db
from app.models import Scenario, House, ScenarioHouse
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioHouseModelCase:
    def test_default_scenario_house(self, default_house, default_scenario):
        # Arrange
        association = create_entity(
            ScenarioHouse,
            house=default_house,
            scenario=default_scenario,
        )
        # Act
        house_from_db = db.session.scalar(
            sa.select(House).where(House.id == association.right_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.left_id)
        )

        # Assert
        assert association.left_id == scenario_from_db.id
        assert association.right_id == house_from_db.id
        assert association.scenario == scenario_from_db
        assert association.house == house_from_db
        assert association.created_at == association.created_at
        assert association.updated_at == association.updated_at
