from app.repository.associations import ScenarioHouseRepo
from app.infrastructure.models.associations import ScenarioHouse
from app.domain.associations import ScenarioHouseDomain
import sqlalchemy as sa
from app import db
from decimal import Decimal

from tests.factory import create_house, create_scenario
from nanoid import generate
import pytest


class TestHouseRepoCase:
    @staticmethod
    def _create_assoc(house_id, scenario_id):
        assoc_domain = ScenarioHouseDomain(
            house_id=house_id,
            scenario_id=scenario_id,
        )
        return ScenarioHouseRepo.create(assoc_domain)

    def test_create_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Create an house and a scenario domain using the factory
        default_interest_rate = Decimal("3.0")
        new_house.interest_rate = default_interest_rate
        assoc_interest_rate = Decimal("5.0")

        # Create Assoc Domain
        assoc_domain = ScenarioHouseDomain(
            house_id=new_house.id,
            scenario_id=new_scenario.id,
            interest_rate=assoc_interest_rate,
        )

        # Act: Save the house domain to the scenario domain by ScenarioHouseRepo, and get the association obj back from database
        scenario_house_from_repo = ScenarioHouseRepo.create(assoc_domain)

        scenario_house_from_db = db.session.scalars(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario_id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_house_from_repo.house_id == scenario_house_from_db.house_id
        assert (
            scenario_house_from_repo.scenario_id == scenario_house_from_db.scenario_id
        )
        assert (
            scenario_house_from_repo.interest_rate
            == scenario_house_from_db.interest_rate
        )
        assert scenario_house_from_repo.interest_rate == assoc_interest_rate

    def test_update_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Adding a house to scenario using the ScenarioHouseRepo
        default_interest_rate = Decimal("5.0")
        assoc_domain = ScenarioHouseDomain(
            house_id=new_house.id,
            scenario_id=new_scenario.id,
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
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario_id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house_id)
            )
        ).one()  # This ensures only one row is returned, or an exception is raised.

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario_house.house_id == scenario_house_from_db.house_id
        assert updated_scenario_house.scenario_id == scenario_house_from_db.scenario_id
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
            house_id=new_house.id,
            scenario_id=new_scenario.id,
        )

        # Act: Update the house domain object (before saving)
        scenario_house_get_by_id = ScenarioHouseRepo.get_by_id(
            scenario_id=scenario_house_from_repo.scenario_id,
            house_id=scenario_house_from_repo.house_id,
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert (
            scenario_house_get_by_id.scenario_id == scenario_house_from_repo.scenario_id
        )
        assert scenario_house_get_by_id.house_id == scenario_house_from_repo.house_id

    def test_get_scenario_house_assoc_list_through_repo(
        self, default_account, new_scenario
    ):
        # Arrange: Create an house domain using the factory
        origin_repo_list_length = len(
            ScenarioHouseRepo.get_list(scenario_id=new_scenario.id)
        )

        # Act: Create 5 new house domains
        for _ in range(5):
            new_house = create_house(default_account)
            self._create_assoc(
                house_id=new_house.id,
                scenario_id=new_scenario.id,
            )

        # Assert: Ensure the list length is increased by 5
        updated_list_length = len(
            ScenarioHouseRepo.get_list(scenario_id=new_scenario.id)
        )
        assert updated_list_length == (origin_repo_list_length + 5)

    def test_delete_scenario_house_assoc_through_repo(self, new_scenario, new_house):
        # Arrange: Create an house domain using the factory
        scenario_house_from_repo = self._create_assoc(
            house_id=new_house.id,
            scenario_id=new_scenario.id,
        )

        # Act: Delete the house domain object
        ScenarioHouseRepo.delete_by_id(
            scenario_id=scenario_house_from_repo.scenario_id,
            house_id=scenario_house_from_repo.house_id,
        )

        # Assert: Ensure the house record is deleted from the database
        scenario_house_from_db = db.session.scalar(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_house_from_repo.scenario_id)
                & (ScenarioHouse.house_id == scenario_house_from_repo.house_id)
            )
        )
        assert scenario_house_from_db is None

    def test_create_scenario_house_assoc_through_repo_with_invalid_input(
        self, new_house
    ):
        # Arrange: Create non-existed scenario ID
        invalid_scenario_id = 10482

        # Act: Create Association with invalid scenario id should raise TypeError
        with pytest.raises(TypeError):
            self._create_assoc(
                house_id=new_house.id,
                scenario_id=invalid_scenario_id,
            )

    def test_create_scenario_house_assoc_through_repo_with_non_existed_scenario(
        self, new_house
    ):
        # Arrange: Create non-existed scenario ID
        non_existed_scenario_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                house_id=new_house.id,
                scenario_id=non_existed_scenario_id,
            )

    def test_create_scenario_house_assoc_through_repo_with_non_existed_house(
        self, new_scenario
    ):
        # Arrange: Create non-existed house ID
        non_existed_house_id = generate(size=13)

        # Act: Create Association with non existed scenario should raise ValueError
        with pytest.raises(ValueError):
            self._create_assoc(
                house_id=non_existed_house_id,
                scenario_id=new_scenario.id,
            )

    def test_get_non_existed_scenario_house_assoc_by_id_through_repo(
        self, new_scenario, new_house
    ):
        # Act: Get the assoc by compose id (but not create association yet)
        scenario_house_get_by_id = ScenarioHouseRepo.get_by_id(
            scenario_id=new_scenario.id,
            house_id=new_house.id,
        )

        # Assert: The ScenarioHouseRepo should return None
        assert scenario_house_get_by_id is None

    def test_update_scenario_house_assoc_through_repo_while_changing_scenario(
        self, new_scenario, new_house, default_account
    ):
        # Arrange: Get scenario and house id
        scenario_id = new_scenario.id
        house_id = new_house.id

        # Arrange: Create Association
        assoc = self._create_assoc(house_id=house_id, scenario_id=scenario_id)

        # Arrange: Create another scenario
        another_scenario = create_scenario(default_account)
        another_scenario_id = another_scenario.id

        # Act: Change the assoc to another scenario id
        assoc.scenario_id = another_scenario_id

        # Assert: Save the updated object should raise ValueError as this assoc is not existed in another scenario
        with pytest.raises(ValueError):
            ScenarioHouseRepo.save(assoc)

    def test_delete_non_existed_scenario_house_assoc_through_repo(
        self, new_scenario, new_house
    ):
        # Arrange: Get scenario and house id
        scenario_id = new_scenario.id
        house_id = new_house.id
        # Act: Delete the non existed assoc
        ScenarioHouseRepo.delete_by_id(
            scenario_id=scenario_id,
            house_id=house_id,
        )

        # Assert: Ensure the house record is deleted from the database
        scenario_house_from_db = db.session.scalar(
            sa.select(ScenarioHouse).where(
                (ScenarioHouse.scenario_id == scenario_id)
                & (ScenarioHouse.house_id == house_id)
            )
        )
        assert scenario_house_from_db is None
