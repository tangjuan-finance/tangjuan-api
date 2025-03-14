from app import db
from app.models import Asset
import sqlalchemy as sa


class TestAssetModelCase:
    def test_create_asset(self, default_asset):
        # Act
        asset_from_db = db.session.scalar(
            sa.select(Asset).where(Asset.id == default_asset.id)
        )

        # Assert
        assert asset_from_db.name == default_asset.name
        assert asset_from_db.amount == default_asset.amount
        assert (
            asset_from_db.max_yearly_return_rate == default_asset.max_yearly_return_rate
        )
        assert (
            asset_from_db.min_yearly_return_rate == default_asset.min_yearly_return_rate
        )
        assert asset_from_db.start_age == default_asset.start_age
        assert asset_from_db.owner_id == default_asset.owner_id
