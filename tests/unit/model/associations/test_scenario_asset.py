from app import db
from app.models import Scenario, Asset, ScenarioAsset
import sqlalchemy as sa
from ..factories import create_entity


class TestScenarioAssetModelCase:
    def test_default_scenario_asset(self, default_asset, default_scenario):
        # Arrange

        allocation_percentage = 0.6

        association = create_entity(
            ScenarioAsset,
            asset=default_asset,
            scenario=default_scenario,
            allocation_percentage=allocation_percentage,
        )
        # Act
        asset_from_db = db.session.scalar(
            sa.select(Asset).where(Asset.id == association.right_id)
        )
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == association.left_id)
        )

        # Assert
        assert association.left_id == scenario_from_db.id
        assert association.right_id == asset_from_db.id
        assert association.scenario == scenario_from_db
        assert association.asset == asset_from_db
        assert association.allocation_percentage == allocation_percentage
