from app.domain.entities import AssetDomain
from decimal import Decimal
from tests.factory import AssetDomainFactory


class TestAssetDomainCase:
    def test_create_asset_domain(self, default_account_domain):
        # Arrange
        name = "Default Asset Domain"
        amount = 50000
        max_yearly_return_rate = Decimal("0.5")
        min_yearly_return_rate = Decimal("-0.5")
        start_age = 20
        end_age = 100

        # Act
        asset = AssetDomain(
            name=name,
            amount=amount,
            max_yearly_return_rate=max_yearly_return_rate,
            min_yearly_return_rate=min_yearly_return_rate,
            start_age=start_age,
            end_age=end_age,
            owner=default_account_domain,
        )

        # Assert
        assert isinstance(asset.id, str)
        assert len(asset.id) == 13
        assert asset.name == name
        assert asset.amount == amount
        assert asset.max_yearly_return_rate == max_yearly_return_rate
        assert asset.min_yearly_return_rate == min_yearly_return_rate
        assert asset.start_age == start_age
        assert asset.owner == default_account_domain

    def test_factory_asset_domain(self):
        # Arrange
        name = "Default Asset Domain"
        amount = 50000
        max_yearly_return_rate = Decimal("0.5")
        min_yearly_return_rate = Decimal("-0.5")
        start_age = 20
        end_age = 100

        # Act
        asset = AssetDomainFactory(
            name=name,
            amount=amount,
            max_yearly_return_rate=max_yearly_return_rate,
            min_yearly_return_rate=min_yearly_return_rate,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert isinstance(asset.id, str)
        assert len(asset.id) == 13
        assert asset.name == name
        assert asset.amount == amount
        assert asset.max_yearly_return_rate == max_yearly_return_rate
        assert asset.min_yearly_return_rate == min_yearly_return_rate
        assert asset.start_age == start_age
