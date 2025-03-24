from app.repository.entities import HouseRepo
from app.infrastructure.models.entities import House
from tests.unit.factories import HouseDomainFactory
import sqlalchemy as sa
from app import db


class TestHouseRepoCase:
    def test_create_house_domain_through_repo(self):
        # Arrange: Create an house domain using the factory
        house = HouseDomainFactory()

        # Act: Save the house domain using the repo and return the saved entity
        house_from_repo = HouseRepo.create(house)
        house_from_db = db.session.scalar(sa.select(House).where(House.id == house.id))

        # Assert: Ensure the values match between the domain object and the saved record
        assert house_from_repo.id == house_from_db.id
        assert house_from_repo.name == house_from_db.name
        assert house_from_repo.amount == house_from_db.amount
        assert house_from_repo.down_payment == house_from_db.down_payment
        assert house_from_repo.interest_rate == house_from_db.interest_rate
        assert house_from_repo.loan_term == house_from_db.loan_term
        assert house_from_repo.purchase_age == house_from_db.purchase_age
        assert house_from_repo.owner == house_from_db.owner
        assert house_from_repo.created_at == house_from_db.created_at
        assert house_from_repo.updated_at == house_from_db.updated_at

    def test_update_house_domain_through_repo(self):
        # Arrange: Create an house domain using the factory
        house = HouseDomainFactory()
        house_from_repo = HouseRepo.create(house)
        updated_name = "Updated House Domain"

        # Act: Update the house domain object (before saving)
        house_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_house = HouseRepo.save(house_from_repo)

        # Query the database to verify the updated house record
        house_from_db = db.session.scalar(
            sa.select(House).where(House.id == house_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_house.id == house_from_db.id
        assert updated_house.name == house_from_db.name
        assert updated_house.created_at == house_from_db.created_at
        assert updated_house.updated_at != house_from_db.updated_at

    def test_get_house_domain_by_id_through_repo(self):
        # Arrange: Create an house domain using the factory
        house = HouseDomainFactory()
        HouseRepo.create(house)

        # Act: Update the house domain object (before saving)
        house_get_by_id = HouseRepo.get_by_id(house.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert house_get_by_id.id == house.id
        assert house_get_by_id.name == house.name

    def test_get_house_domain_list_through_repo(self):
        # Arrange: Create an house domain using the factory
        origin_house_list_length = len(HouseRepo.get_list())

        # Act: Create 5 new house domains
        for _ in range(5):
            house = HouseDomainFactory()
            HouseRepo.create(house)

        # Assert: Ensure the list length is increased by 5
        updated_house_list_length = len(HouseRepo.get_list())
        assert updated_house_list_length == (origin_house_list_length + 5)

    def test_delete_house_domain_through_repo(self):
        # Arrange: Create an house domain using the factory
        house = HouseDomainFactory()
        house_from_repo = HouseRepo.create(house)

        # Act: Delete the house domain object
        HouseRepo.delete(house_from_repo)

        # Assert: Ensure the house record is deleted from the database
        assert (
            db.session.scalar(sa.select(House).where(House.id == house_from_repo.id))
            is None
        )
