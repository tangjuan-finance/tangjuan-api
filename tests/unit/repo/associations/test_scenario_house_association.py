from app.repository.associations import ScenarioHouseRepo
from app.infrastructure.models.associations import ScenarioHouse
from app.domain.associations import ScenarioHouseDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.unit.repo.factories import create_scenario, create_house


class TestHouseRepoCase:
    @staticmethod
    def _create_assoc(house, scenario):
        assoc_domain = ScenarioHouseDomain(
            house=house,
            scenario=scenario,
        )
        return ScenarioHouseRepo.create(assoc_domain)

    def test_create_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Create an house and a scenario domain using the factory
        default_interest_rate = Decimal("3.0")
        new_house.interest_rate = default_interest_rate
        assoc_interest_rate = Decimal("5.0")
        assoc_domain = ScenarioHouseDomain(
            house=new_house,
            scenario=new_scenario,
            interest_rate=assoc_interest_rate,
        )

        # Act: Save the house domain to the scenario domain by ScenarioHouseRepo, and get the association obj back from database
        scenario_house_from_repo = ScenarioHouseRepo.create(assoc_domain)

        scenario_house_from_db = db.session.scalars(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario.id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_house_from_repo.house.id == scenario_house_from_db.house_id
        assert (
            scenario_house_from_repo.scenario.id == scenario_house_from_db.scenario_id
        )
        assert (
            scenario_house_from_repo.interest_rate
            == scenario_house_from_db.interest_rate
        )
        assert scenario_house_from_repo.interest_rate == assoc_interest_rate
        assert scenario_house_from_repo.house.interest_rate == default_interest_rate
        assert (
            scenario_house_from_repo.interest_rate
            != scenario_house_from_repo.house.interest_rate
        )

    def test_update_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Adding a house to scenario using the ScenarioHouseRepo
        default_interest_rate = Decimal("7.0")
        assoc_domain = ScenarioHouseDomain(
            house=new_house,
            scenario=new_scenario,
            interest_rate=default_interest_rate,
        )
        scenario_house_from_repo = ScenarioHouseRepo.create(assoc_domain)
        updated_interest_rate = Decimal("3.0")

        # Act: Update the house domain object (before saving)
        scenario_house_from_repo.interest_rate = updated_interest_rate

        # Save the updated object through the repository and get the result
        updated_scenario_house = ScenarioHouseRepo.save(scenario_house_from_repo)

        # Query the database to verify the updated house record
        scenario_house_from_db = db.session.scalars(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario.id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house.id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_house.house.id == scenario_house_from_db.house_id
        assert updated_scenario_house.scenario.id == scenario_house_from_db.scenario_id
        assert updated_scenario_house.interest_rate == updated_interest_rate
        assert (
            updated_scenario_house.interest_rate == scenario_house_from_db.interest_rate
        )
        assert updated_scenario_house.created_at == scenario_house_from_db.created_at
        assert updated_scenario_house.updated_at == scenario_house_from_db.updated_at
        # Update_at from updated_house should be different from the previous house domain (the one before update)
        assert updated_scenario_house.updated_at > scenario_house_from_repo.updated_at

    def test_get_scenario_house_assoc_by_id_through_repo(self, new_scenario, new_house):
        # Arrange: Create an house domain using the factory
        scenario_house_from_repo = self._create_assoc(
            house=new_house, scenario=new_scenario
        )

        # Act: Update the house domain object (before saving)
        scenario_house_get_by_id = ScenarioHouseRepo.get_by_id(
            scenario_id=scenario_house_from_repo.scenario.id,
            house_id=scenario_house_from_repo.house.id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_house_get_by_id.scenario.id == scenario_house_from_repo.scenario.id
        )
        assert scenario_house_get_by_id.house.id == scenario_house_from_repo.house.id

    def test_get_scenario_house_assoc_list_through_repo(self, default_account):
        # Arrange: Create an house domain using the factory
        origin_repo_list_length = len(ScenarioHouseRepo.get_list())

        # Act: Create 5 new house domains
        for _ in range(5):
            new_scenario = create_scenario(default_account)
            new_house = create_house(default_account)
            self._create_assoc(house=new_house, scenario=new_scenario)

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(ScenarioHouseRepo.get_list())
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Create an house domain using the factory
        scenario_house_from_repo = self._create_assoc(
            house=new_house, scenario=new_scenario
        )

        # Act: Delete the house domain object
        ScenarioHouseRepo.delete_by_id(
            scenario_id=scenario_house_from_repo.scenario.id,
            house_id=scenario_house_from_repo.house.id,
        )

        # Assert: Ensure the house record is deleted from the database
        scenario_house_from_db = db.session.scalar(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario.id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house.id)
            )
        )
        assert scenario_house_from_db is None
