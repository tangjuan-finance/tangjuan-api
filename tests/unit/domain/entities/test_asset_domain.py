# from app.domain.entities import AssetDomain
from decimal import Decimal


class TestAssetDomainCase:
    def test_create_asset_domain(default_asset_domain, default_account_domain):
        # Assert
        assert default_asset_domain.name == "Default Asset Domain"
        assert default_asset_domain.amount == 50000
        assert default_asset_domain.max_yearly_return_rate == Decimal("0.5")
        assert default_asset_domain.min_yearly_return_rate == Decimal("-0.5")
        assert default_asset_domain.start_age == 20
        assert default_asset_domain.owner_id == default_account_domain.id
