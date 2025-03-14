from app import db
from app.models import Asset
import sqlalchemy as sa
from .factories import create_entity


class TestAssetModelCase:
    def test_create_asset(self, default_account):
        # Arrange
        name = "Default Asset"
        amount = 50000
        max_yearly_return_rate = 0.5
        min_yearly_return_rate = -0.5
        start_age = 20

        asset = create_entity(
            Asset,
            owner=default_account,
            name=name,
            amount=amount,
            max_yearly_return_rate=max_yearly_return_rate,
            min_yearly_return_rate=min_yearly_return_rate,
            start_age=start_age,
        )
        # Act
        asset_from_db = db.session.scalar(
            sa.select(Asset).where(Asset.name == Asset.name)
        )

        # Assert
        assert asset_from_db.amount == asset.amount
        assert asset_from_db.owner_id == asset.owner_id
