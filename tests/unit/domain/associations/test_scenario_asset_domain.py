from app.domain.associations import ScenarioAssetDomain
from tests.factory import create_fake_id
from decimal import Decimal
from datetime import datetime, timezone


class TestAssetDomainCase:
    def test_create_scenario_asset_domain(self):
        # Arrange
        max_yearly_return_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")
        scenario_id = create_fake_id()
        asset_id = create_fake_id()

        # Act
        scenario_asset = ScenarioAssetDomain(
            scenario_id=scenario_id,
            asset_id=asset_id,
            max_yearly_return_rate=max_yearly_return_rate,
            allocation_percentage=allocation_percentage,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_asset.scenario_id == scenario_id
        assert scenario_asset.asset_id == asset_id
        assert scenario_asset.max_yearly_return_rate == max_yearly_return_rate
        assert scenario_asset.allocation_percentage == allocation_percentage
