from tests.unit.factories import ScenarioDomainFactory
from app.repository.entities import ScenarioRepo
from app.infrastructure.models.entities import Scenario
import sqlalchemy as sa
from app import db


class TestScenarioDomainCase:
    def test_create_scenario_domain_through_repo(self, default_account):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory(owner=default_account)

        # Act: Save the scenario domain using the repo and return the saved entity
        scenario_from_repo = ScenarioRepo.create(scenario)
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_from_repo.id == scenario_from_db.id
        assert scenario_from_repo.name == scenario_from_db.name
        assert (
            scenario_from_repo.asset_allocation_percentage
            == scenario_from_db.asset_allocation_percentage
        )
        assert scenario_from_repo.retire_age == scenario_from_db.retire_age
        assert scenario_from_repo.owner.id == scenario_from_db.owner.id
        assert scenario_from_repo.created_at == scenario_from_db.created_at
        assert scenario_from_repo.updated_at == scenario_from_db.updated_at

    def test_update_scenario_domain_through_repo(self, default_account):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory(owner=default_account)
        scenario_from_repo = ScenarioRepo.create(scenario)
        updated_name = "Updated Scenario Domain"

        # Act: Update the scenario domain object (before saving)
        scenario_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_scenario = ScenarioRepo.save(scenario_from_repo)

        # Query the database to verify the updated scenario record
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario.id == scenario_from_db.id
        assert updated_scenario.name == scenario_from_db.name
        assert updated_scenario.created_at == scenario_from_db.created_at
        assert updated_scenario.updated_at == scenario_from_db.updated_at
        # Update_at from updated_scenario should be different from the previous scenario domain (the one before update)
        assert updated_scenario.updated_at != scenario_from_repo.updated_at

    def test_get_scenario_domain_by_id_through_repo(self, default_account):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory(owner=default_account)
        scenario_from_repo = ScenarioRepo.create(scenario)

        # Act: Update the scenario domain object (before saving)
        scenario_get_by_id = ScenarioRepo.get_by_id(scenario_from_repo.id)

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert scenario_get_by_id.id == scenario_from_repo.id
        assert scenario_get_by_id.name == scenario_from_repo.name

    def test_get_scenario_domain_list_through_repo(self, default_account):
        # Arrange: Create an scenario domain using the factory
        origin_scenario_list_length = len(ScenarioRepo.get_list())

        # Act: Create 5 new scenario domains
        for _ in range(5):
            scenario = ScenarioDomainFactory(owner=default_account)
            ScenarioRepo.create(scenario)

        # Assert: Ensure the list length is increased by 5
        updated_scenario_list_length = len(ScenarioRepo.get_list())
        assert updated_scenario_list_length == (origin_scenario_list_length + 5)

    def test_delete_scenario_domain_through_repo(self, default_account):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory(owner=default_account)
        scenario_from_repo = ScenarioRepo.create(scenario)

        # Act: Delete the scenario domain object
        ScenarioRepo.delete_by_id(scenario_from_repo.id)

        # Assert: Ensure the scenario record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(Scenario).where(Scenario.id == scenario_from_repo.id)
            )
            is None
        )
