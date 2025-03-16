from app import db
from app.infrastructure.models import Scenario
import sqlalchemy as sa


class TestScenarioModelCase:
    def test_default_scenario(self, default_scenario):
        # Act
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == default_scenario.id)
        )

        # Assert
        assert scenario_from_db.name == default_scenario.name
        assert (
            scenario_from_db.asset_allocation_percentage
            == default_scenario.asset_allocation_percentage
        )
        assert scenario_from_db.retire_age == default_scenario.retire_age
        assert scenario_from_db.created_at == default_scenario.created_at
        assert scenario_from_db.updated_at == default_scenario.updated_at
        assert scenario_from_db.owner_id == default_scenario.owner_id
