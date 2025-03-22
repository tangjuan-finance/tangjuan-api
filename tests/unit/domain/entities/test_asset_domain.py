# from app.domain.entities import AssetDomain
from decimal import Decimal
from tests.unit.factories import AssetDomainFactory


class TestAssetDomainCase:
    def test_create_asset_domain(self, default_asset_domain, default_account_domain):
        # Assert
        assert default_asset_domain.name == "Default Asset Domain"
        assert default_asset_domain.amount == 50000
        assert default_asset_domain.max_yearly_return_rate == Decimal("0.5")
        assert default_asset_domain.min_yearly_return_rate == Decimal("-0.5")
        assert default_asset_domain.start_age == 20
        assert default_asset_domain.owner == default_account_domain

    def test_factory_asset_domain(self):
        # Arrange
        name = "Default Asset Domain"
        amount = 50000
        max_yearly_return_rate = Decimal("0.5")
        min_yearly_return_rate = Decimal("-0.5")
        start_age = 20

        # Act
        asset = AssetDomainFactory(
            name=name,
            amount=amount,
            max_yearly_return_rate=max_yearly_return_rate,
            min_yearly_return_rate=min_yearly_return_rate,
            start_age=start_age,
        )

        # Assert
        assert asset.name == name
        assert asset.amount == amount
        assert asset.max_yearly_return_rate == max_yearly_return_rate
        assert asset.min_yearly_return_rate == min_yearly_return_rate
        assert asset.start_age == start_age
