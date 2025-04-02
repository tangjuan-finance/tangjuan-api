from app.repository.associations import ScenarioAssetRepo
from app.infrastructure.models.associations import ScenarioAsset
from app.domain.associations import ScenarioAssetDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.factory import create_asset, create_scenario
from nanoid import generate
import pytest


class TestAssetRepoCase:
    @staticmethod
    def _create_assoc(asset_id, scenario_id, allocation_percentage):
        assoc_domain = ScenarioAssetDomain(
            asset_id=asset_id,
            scenario_id=scenario_id,
            allocation_percentage=allocation_percentage,
        )
        return ScenarioAssetRepo.create(assoc_domain)

    def test_create_scenario_asset_assoc_through_repo(self, new_scenario, new_asset):
        # Arrange: Create an asset and a scenario domain using the factory
        default_max_yearly_return_rate = Decimal("0.2")
        new_asset.max_yearly_return_rate = default_max_yearly_return_rate
        assoc_max_yearly_return_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")

        # Create Assoc Domain
        assoc_domain = ScenarioAssetDomain(
            asset_id=new_asset.id,
            scenario_id=new_scenario.id,
            max_yearly_return_rate=assoc_max_yearly_return_rate,
            allocation_percentage=allocation_percentage,
        )

        # Act: Save the asset domain to the scenario domain by ScenarioAssetRepo, and get the association obj back from database
        scenario_asset_from_repo = ScenarioAssetRepo.create(assoc_domain)

        scenario_asset_from_db = db.session.scalars(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario_id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_asset_from_repo.asset_id == scenario_asset_from_db.asset_id
        assert (
            scenario_asset_from_repo.scenario_id == scenario_asset_from_db.scenario_id
        )
        assert (
            scenario_asset_from_repo.max_yearly_return_rate
            == scenario_asset_from_db.max_yearly_return_rate
        )
        assert scenario_asset_from_repo.allocation_percentage == allocation_percentage
        assert (
            scenario_asset_from_repo.allocation_percentage
            == scenario_asset_from_db.allocation_percentage
        )
        assert (
            scenario_asset_from_repo.max_yearly_return_rate
            == assoc_max_yearly_return_rate
        )

    def test_update_scenario_asset_assoc_through_repo(self, new_scenario, new_asset):
        # Arrange: Adding a asset to scenario using the ScenarioAssetRepo
        default_max_yearly_return_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")
        assoc_domain = ScenarioAssetDomain(
            asset_id=new_asset.id,
            scenario_id=new_scenario.id,
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
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario_id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_asset.asset_id == scenario_asset_from_db.asset_id
        assert updated_scenario_asset.scenario_id == scenario_asset_from_db.scenario_id
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

    def test_get_scenario_asset_assoc_by_id_through_repo(self, new_scenario, new_asset):
        # Arrange: Create an asset domain using the factory
        scenario_asset_from_repo = self._create_assoc(
            asset_id=new_asset.id,
            scenario_id=new_scenario.id,
            allocation_percentage=Decimal("0.35"),
        )

        # Act: Update the asset domain object (before saving)
        scenario_asset_get_by_id = ScenarioAssetRepo.get_by_id(
            scenario_id=scenario_asset_from_repo.scenario_id,
            asset_id=scenario_asset_from_repo.asset_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_asset_get_by_id.scenario_id == scenario_asset_from_repo.scenario_id
        )
        assert scenario_asset_get_by_id.asset_id == scenario_asset_from_repo.asset_id

    def test_get_scenario_asset_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an asset domain using the factory
        origin_repo_list_length = len(
            ScenarioAssetRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new asset domains
        for _ in range(5):
            new_asset = create_asset(default_account)
            self._create_assoc(
                asset_id=new_asset.id,
                scenario_id=new_scenario.id,
                allocation_percentage=Decimal("0.35"),
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioAssetRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_asset_assoc_through_repo(self, new_scenario, new_asset):
        # Arrange: Create an asset domain using the factory
        scenario_asset_from_repo = self._create_assoc(
            asset_id=new_asset.id,
            scenario_id=new_scenario.id,
            allocation_percentage=Decimal("0.35"),
        )

        # Act: Delete the asset domain object
        ScenarioAssetRepo.delete_by_id(
            scenario_id=scenario_asset_from_repo.scenario_id,
            asset_id=scenario_asset_from_repo.asset_id,
        )

        # Assert: Ensure the asset record is deleted from the database
        scenario_asset_from_db = db.session.scalar(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_asset_from_repo.scenario_id)
                & (ScenarioAsset.asset_id == scenario_asset_from_repo.asset_id)
            )
        )
        assert scenario_asset_from_db is None

    def test_create_scenario_asset_assoc_through_repo_with_invalid_input(
        self, new_asset
    ):
        # Arrange: Create non-existed scenario ID
        invalid_scenario_id = 10482

        # Act: Create Association with invalid scenario id should raise TypeError
        with pytest.raises(TypeError):
            self._create_assoc(
                asset_id=new_asset.id,
                scenario_id=invalid_scenario_id,
                allocation_percentage=Decimal("0.35"),
            )

    def test_create_scenario_asset_assoc_through_repo_with_non_existed_scenario(
        self, new_asset
    ):
        # Arrange: Create non-existed scenario ID
        non_existed_scenario_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                asset_id=new_asset.id,
                scenario_id=non_existed_scenario_id,
                allocation_percentage=Decimal("0.35"),
            )

    def test_create_scenario_asset_assoc_through_repo_with_non_existed_asset(
        self, new_scenario
    ):
        # Arrange: Create non-existed asset ID
        non_existed_asset_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                asset_id=non_existed_asset_id,
                scenario_id=new_scenario.id,
                allocation_percentage=Decimal("0.35"),
            )

    def test_get_non_existed_scenario_asset_assoc_by_id_through_repo(
        self, new_scenario, new_asset
    ):
        # Act: Get the assoc by compose id (but not create association yet)
        scenario_asset_get_by_id = ScenarioAssetRepo.get_by_id(
            scenario_id=new_scenario.id,
            asset_id=new_asset.id,
        )

        # Assert: The ScenarioAssetRepo should return None
        assert scenario_asset_get_by_id is None

    def test_update_scenario_asset_assoc_through_repo_while_changing_scenario(
        self, new_scenario, new_asset, default_account
    ):
        # Arrange: Get scenario and asset id
        scenario_id = new_scenario.id
        asset_id = new_asset.id

        # Arrange: Create Association
        assoc = self._create_assoc(
            asset_id=asset_id,
            scenario_id=scenario_id,
            allocation_percentage=Decimal("0.35"),
        )

        # Arrange: Create another scenario
        another_scenario = create_scenario(default_account)
        another_scenario_id = another_scenario.id

        # Act: Change the assoc to another scenario id
        assoc.scenario_id = another_scenario_id

        # Assert: Save the updated object should raise ValueError as this assoc is not existed in another scenario
        with pytest.raises(ValueError):
            ScenarioAssetRepo.save(assoc)

    def test_delete_non_existed_scenario_asset_assoc_through_repo(
        self, new_scenario, new_asset
    ):
        # Arrange: Get scenario and asset id
        scenario_id = new_scenario.id
        asset_id = new_asset.id
        # Act: Delete the non existed assoc
        ScenarioAssetRepo.delete_by_id(
            scenario_id=scenario_id,
            asset_id=asset_id,
        )

        # Assert: Ensure the asset record is deleted from the database
        scenario_asset_from_db = db.session.scalar(
            sa.select(ScenarioAsset).where(
                (ScenarioAsset.scenario_id == scenario_id)
                & (ScenarioAsset.asset_id == asset_id)
            )
        )
        assert scenario_asset_from_db is None
