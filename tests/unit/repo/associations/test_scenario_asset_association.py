from app.repository.associations import ScenarioAssetRepo
from app.infrastructure.models.associations import ScenarioAsset
from app.domain.associations import ScenarioAssetDomain
from tests.unit.factories import AssetDomainFactory, ScenarioDomainFactory
import sqlalchemy as sa
from app import db
from decimal import Decimal


class TestAssetRepoCase:
    def _create_assoc(self, default_account):
        scenario = ScenarioDomainFactory(owner=default_account)
        asset = AssetDomainFactory(owner=default_account)
        allocation_percentage = Decimal("0.35")
        assoc_domain = ScenarioAssetDomain(
            asset=asset,
            scenario=scenario,
            allocation_percentage=allocation_percentage,
        )
        return ScenarioAssetRepo.create(assoc_domain)

    def test_create_scenario_asset_assoc_through_repo(self, default_account):
        # Arrange: Create an asset and a scenario domain using the factory
        default_max_yearly_return_rate = Decimal("0.2")
        scenario = ScenarioDomainFactory(owner=default_account)
        allocation_percentage = Decimal("0.35")
        asset = AssetDomainFactory(
            owner=default_account, max_yearly_return_rate=default_max_yearly_return_rate
        )
        assoc_max_yearly_return_rate = Decimal("0.7")
        assoc_domain = ScenarioAssetDomain(
            asset=asset,
            scenario=scenario,
            max_yearly_return_rate=assoc_max_yearly_return_rate,
            allocation_percentage=allocation_percentage,
        )

        # Act: Save the asset domain to the scenario domain by ScenarioAssetRepo, and get the association obj back from database
        scenario_asset_from_repo = ScenarioAssetRepo.create(assoc_domain)

        scenario_asset_from_db = db.session.scalar(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario.id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_asset_from_repo.allocation_percentage == allocation_percentage
        assert scenario_asset_from_repo.asset.id == scenario_asset_from_db.asset_id
        assert (
            scenario_asset_from_repo.scenario.id == scenario_asset_from_db.scenario_id
        )
        assert (
            scenario_asset_from_repo.max_yearly_return_rate
            == scenario_asset_from_db.max_yearly_return_rate
        )
        assert (
            scenario_asset_from_repo.max_yearly_return_rate
            == assoc_max_yearly_return_rate
        )
        assert (
            scenario_asset_from_repo.asset.max_yearly_return_rate
            == default_max_yearly_return_rate
        )
        assert (
            scenario_asset_from_repo.max_yearly_return_rate
            != scenario_asset_from_repo.asset.max_yearly_return_rate
        )

    def test_update_scenario_asset_assoc_through_repo(self, default_account):
        # Arrange: Adding a asset to scenario using the ScenarioAssetRepo
        scenario = ScenarioDomainFactory(owner=default_account)
        asset = AssetDomainFactory(owner=default_account)
        default_max_yearly_return_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")
        assoc_domain = ScenarioAssetDomain(
            asset=asset,
            scenario=scenario,
            max_yearly_return_rate=default_max_yearly_return_rate,
            allocation_percentage=allocation_percentage,
        )
        scenario_asset_from_repo = ScenarioAssetRepo.create(assoc_domain)
        updated_max_yearly_return_rate = Decimal("0.3")

        # Act: Update the asset domain object (before saving)
        scenario_asset_from_repo.max_yearly_return_rate = updated_max_yearly_return_rate

        # Save the updated object through the repository and get the result
        updated_scenario_asset = ScenarioAssetRepo.save(scenario_asset_from_repo)

        # Query the database to verify the updated asset record
        scenario_asset_from_db = db.session.scalars(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario.id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_asset.asset.id == scenario_asset_from_db.asset_id
        assert updated_scenario_asset.scenario.id == scenario_asset_from_db.scenario_id
        assert (
            updated_scenario_asset.max_yearly_return_rate
            == updated_max_yearly_return_rate
        )
        assert (
            updated_scenario_asset.max_yearly_return_rate
            == scenario_asset_from_db.max_yearly_return_rate
        )
        assert updated_scenario_asset.created_at == scenario_asset_from_db.created_at
        assert updated_scenario_asset.updated_at == scenario_asset_from_db.updated_at
        # Update_at from updated_asset should be different from the previous asset domain (the one before update)
        assert updated_scenario_asset.updated_at > scenario_asset_from_repo.updated_at

    def test_get_scenario_asset_assoc_by_id_through_repo(self, default_account):
        # Arrange: Create an asset domain using the factory
        scenario_asset_from_repo = self._create_assoc(default_account)

        # Act: Update the asset domain object (before saving)
        scenario_asset_get_by_id = ScenarioAssetRepo.get_by_id(
            scenario_id=scenario_asset_from_repo.scenario.id,
            asset_id=scenario_asset_from_repo.asset.id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_asset_get_by_id.scenario_id == scenario_asset_from_repo.scenario_id
        )
        assert scenario_asset_get_by_id.asset_id == scenario_asset_from_repo.asset_id

    def test_get_scenario_asset_assoc_list_through_repo(self, default_account):
        # Arrange: Create an asset domain using the factory
        origin_repo_list_length = len(ScenarioAssetRepo.get_list())

        # Act: Create 5 new asset domains
        for _ in range(5):
            self._create_assoc(default_account)

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(ScenarioAssetRepo.get_list())
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_asset_assoc_through_repo(self, default_account):
        # Arrange: Create an asset domain using the factory
        scenario_asset_from_repo = self._create_assoc(default_account)

        # Act: Delete the asset domain object
        ScenarioAssetRepo.delete_by_id(scenario_asset_from_repo.id)

        # Assert: Ensure the asset record is deleted from the database
        scenario_asset_from_db = db.session.scalars(
            sa.select(ScenarioAssetRepo).where(
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario.id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset.id)
            )
        )
        assert scenario_asset_from_db is None
