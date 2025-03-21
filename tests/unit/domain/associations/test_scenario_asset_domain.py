from app.domain.associations import ScenarioAssetDomain
from tests.unit.factories import AssetDomainFactory
from decimal import Decimal


class TestAssetDomainCase:
    def test_create_asset_domain(default_asset_domain, default_account_domain):
        # Arrange
        default_max_yearly_return_rate = Decimal("0.2")
        asset = AssetDomainFactory(
            name="asset", max_yearly_return_rate=default_max_yearly_return_rate
        )
        max_yearly_return_rate = Decimal("0.7")
        # Act
        scenario_asset = ScenarioAssetDomain(
            asset=asset,
            max_yearly_return_rate=max_yearly_return_rate,
        )
        # Assert
        assert scenario_asset.asset.name == "asset"
        assert scenario_asset.max_yearly_return_rate != default_max_yearly_return_rate
        assert scenario_asset.max_yearly_return_rate == max_yearly_return_rate
