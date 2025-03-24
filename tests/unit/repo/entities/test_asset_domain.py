from app.repository.entities import AssetRepo
from app.infrastructure.models.entities import Asset
from tests.unit.factories import AssetDomainFactory
import sqlalchemy as sa
from app import db


class TestAssetRepoCase:
    def test_create_asset_domain_through_repo(self):
        # Arrange: Create an asset domain using the factory
        asset = AssetDomainFactory()

        # Act: Save the asset domain using the repo and return the saved entity
        asset_from_repo = AssetRepo.create(asset)
        asset_from_db = db.session.scalar(sa.select(Asset).where(Asset.id == asset.id))

        # Assert: Ensure the values match between the domain object and the saved record
        assert asset_from_repo.id == asset_from_db.id
        assert asset_from_repo.name == asset_from_db.name
        assert asset_from_repo.amount == asset_from_db.amount
        assert (
            asset_from_repo.max_yearly_return_rate
            == asset_from_db.max_yearly_return_rate
        )
        assert (
            asset_from_repo.min_yearly_return_rate
            == asset_from_db.min_yearly_return_rate
        )
        assert asset_from_repo.start_age == asset_from_db.start_age
        assert asset_from_repo.owner == asset_from_db.owner
        assert asset_from_repo.created_at == asset_from_db.created_at
        assert asset_from_repo.updated_at == asset_from_db.updated_at

    def test_update_asset_domain_through_repo(self):
        # Arrange: Create an asset domain using the factory
        asset = AssetDomainFactory()
        asset_from_repo = AssetRepo.create(asset)
        updated_name = "Updated Asset Domain"

        # Act: Update the asset domain object (before saving)
        asset_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_asset = AssetRepo.save(asset_from_repo)

        # Query the database to verify the updated asset record
        asset_from_db = db.session.scalar(
            sa.select(Asset).where(Asset.id == asset_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_asset.id == asset_from_db.id
        assert updated_asset.name == asset_from_db.name
        assert updated_asset.created_at == asset_from_db.created_at
        assert updated_asset.updated_at != asset_from_db.updated_at

    def test_get_asset_domain_by_id_through_repo(self):
        # Arrange: Create an asset domain using the factory
        asset = AssetDomainFactory()
        AssetRepo.create(asset)

        # Act: Update the asset domain object (before saving)
        asset_get_by_id = AssetRepo.get_by_id(asset.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert asset_get_by_id.id == asset.id
        assert asset_get_by_id.name == asset.name

    def test_get_asset_domain_list_through_repo(self):
        # Arrange: Create an asset domain using the factory
        origin_asset_list_length = len(AssetRepo.get_list())

        # Act: Create 5 new asset domains
        for _ in range(5):
            asset = AssetDomainFactory()
            AssetRepo.create(asset)

        # Assert: Ensure the list length is increased by 5
        updated_asset_list_length = len(AssetRepo.get_list())
        assert updated_asset_list_length == (origin_asset_list_length + 5)

    def test_delete_asset_domain_through_repo(self):
        # Arrange: Create an asset domain using the factory
        asset = AssetDomainFactory()
        asset_from_repo = AssetRepo.create(asset)

        # Act: Delete the asset domain object
        AssetRepo.delete(asset_from_repo)

        # Assert: Ensure the asset record is deleted from the database
        assert (
            db.session.scalar(sa.select(Asset).where(Asset.id == asset_from_repo.id))
            is None
        )
