from app.domain.associations import ScenarioAssetDomain
from tests.unit.factories import AssetDomainFactory
from decimal import Decimal
from datetime import datetime, timezone


class TestAssetDomainCase:
    def test_create_scenario_asset_domain(self, default_scenario_domain):
        # Arrange
        name = "asset for scenario"

        default_max_yearly_return_rate = Decimal("0.2")
        asset = AssetDomainFactory(
            name=name, max_yearly_return_rate=default_max_yearly_return_rate
        )
        max_yearly_return_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")

        # Act
        scenario_asset = ScenarioAssetDomain(
            scenario_id=default_scenario_domain.id,
            asset_id=asset.id,
            max_yearly_return_rate=max_yearly_return_rate,
            allocation_percentage=allocation_percentage,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_asset.scenario_id == default_scenario_domain.id
        assert scenario_asset.asset_id == asset.id
        assert scenario_asset.max_yearly_return_rate != default_max_yearly_return_rate
        assert scenario_asset.max_yearly_return_rate == max_yearly_return_rate
        assert scenario_asset.allocation_percentage == allocation_percentage
