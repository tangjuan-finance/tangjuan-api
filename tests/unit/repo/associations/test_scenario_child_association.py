from app.repository.associations import ScenarioChildRepo
from app.infrastructure.models.associations import ScenarioChild
from app.domain.associations import ScenarioChildDomain
import sqlalchemy as sa
from app import db

from tests.unit.repo.factories import create_child


class TestChildRepoCase:
    @staticmethod
    def _create_assoc(child_id, scenario_id):
        assoc_domain = ScenarioChildDomain(
            child_id=child_id,
            scenario_id=scenario_id,
        )
        return ScenarioChildRepo.create(assoc_domain)

    def test_create_scenario_child_assoc_through_repo(self, new_scenario, new_child):
        # Arrange: Create an child and a scenario domain using the factory
        default_birth_age = 26
        new_child.birth_age = default_birth_age
        assoc_birth_age = 28

        # Create Assoc Domain
        assoc_domain = ScenarioChildDomain(
            child_id=new_child.id,
            scenario_id=new_scenario.id,
            birth_age=assoc_birth_age,
        )

        # Act: Save the child domain to the scenario domain by ScenarioChildRepo, and get the association obj back from database
        scenario_child_from_repo = ScenarioChildRepo.create(assoc_domain)

        scenario_child_from_db = db.session.scalars(
            sa.select(ScenarioChild).where(
                (ScenarioChild.scenario_id == scenario_child_from_repo.scenario_id)
                & (ScenarioChild.child_id == scenario_child_from_repo.child_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_child_from_repo.child_id == scenario_child_from_db.child_id
        assert (
            scenario_child_from_repo.scenario_id == scenario_child_from_db.scenario_id
        )
        assert scenario_child_from_repo.birth_age == scenario_child_from_db.birth_age
        assert scenario_child_from_repo.birth_age == assoc_birth_age

    def test_update_scenario_child_assoc_through_repo(self, new_scenario, new_child):
        # Arrange: Adding a child to scenario using the ScenarioChildRepo
        default_birth_age = 28
        assoc_domain = ScenarioChildDomain(
            child_id=new_child.id,
            scenario_id=new_scenario.id,
            birth_age=default_birth_age,
        )
        scenario_child_from_repo = ScenarioChildRepo.create(assoc_domain)
        updated_birth_age = 26

        # Act: Update the child domain object (before saving)
        scenario_child_from_repo.birth_age = updated_birth_age

        # Save the updated object through the repository and get the result
        updated_scenario_child = ScenarioChildRepo.save(scenario_child_from_repo)

        # Query the database to verify the updated child record
        scenario_child_from_db = db.session.scalars(
            sa.select(ScenarioChild).where(
                (ScenarioChild.scenario_id == scenario_child_from_repo.scenario_id)
                & (ScenarioChild.child_id == scenario_child_from_repo.child_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_child.child_id == scenario_child_from_db.child_id
        assert updated_scenario_child.scenario_id == scenario_child_from_db.scenario_id
        assert updated_scenario_child.birth_age == updated_birth_age
        assert updated_scenario_child.birth_age == scenario_child_from_db.birth_age
        assert updated_scenario_child.created_at == scenario_child_from_db.created_at
        assert updated_scenario_child.updated_at == scenario_child_from_db.updated_at
        # Update_at from updated_child should be different from the previous child domain (the one before update)
        assert updated_scenario_child.updated_at > scenario_child_from_repo.updated_at

    def test_get_scenario_child_assoc_by_id_through_repo(self, new_scenario, new_child):
        # Arrange: Create an child domain using the factory
        scenario_child_from_repo = self._create_assoc(
            child_id=new_child.id,
            scenario_id=new_scenario.id,
        )

        # Act: Update the child domain object (before saving)
        scenario_child_get_by_id = ScenarioChildRepo.get_by_id(
            scenario_id=scenario_child_from_repo.scenario_id,
            child_id=scenario_child_from_repo.child_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_child_get_by_id.scenario_id == scenario_child_from_repo.scenario_id
        )
        assert scenario_child_get_by_id.child_id == scenario_child_from_repo.child_id

    def test_get_scenario_child_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an child domain using the factory
        origin_repo_list_length = len(
            ScenarioChildRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new child domains
        for _ in range(5):
            new_child = create_child(default_account)
            self._create_assoc(
                child_id=new_child.id,
                scenario_id=new_scenario.id,
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioChildRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_child_assoc_through_repo(self, new_scenario, new_child):
        # Arrange: Create an child domain using the factory
        scenario_child_from_repo = self._create_assoc(
            child_id=new_child.id,
            scenario_id=new_scenario.id,
        )

        # Act: Delete the child domain object
        ScenarioChildRepo.delete_by_id(
            scenario_id=scenario_child_from_repo.scenario_id,
            child_id=scenario_child_from_repo.child_id,
        )

        # Assert: Ensure the child record is deleted from the database
        scenario_child_from_db = db.session.scalar(
            sa.select(ScenarioChild).where(
                (ScenarioChild.scenario_id == scenario_child_from_repo.scenario_id)
                & (ScenarioChild.child_id == scenario_child_from_repo.child_id)
            )
        )
        assert scenario_child_from_db is None
