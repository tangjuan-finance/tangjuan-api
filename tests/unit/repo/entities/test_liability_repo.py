from app.repository.entities import LiabilityRepo
from app.infrastructure.models.entities import Liability
from tests.factory import LiabilityDomainFactory
import sqlalchemy as sa
from app import db


class TestLiabilityRepoCase:
    def test_create_liability_domain_through_repo(self, default_account):
        # Arrange: Create an liability domain using the factory
        liability = LiabilityDomainFactory(owner=default_account)

        # Act: Save the liability domain using the repo and return the saved entity
        liability_from_repo = LiabilityRepo.create(liability)
        liability_from_db = db.session.scalars(
            sa.select(Liability).where(Liability.id == liability_from_repo.id)
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert liability_from_repo.id == liability_from_db.id
        assert liability_from_repo.name == liability_from_db.name
        assert (
            liability_from_repo.principal_amount == liability_from_db.principal_amount
        )
        assert liability_from_repo.interest_rate == liability_from_db.interest_rate
        assert liability_from_repo.start_age == liability_from_db.start_age
        assert liability_from_repo.end_age == liability_from_db.end_age
        assert liability_from_repo.owner.id == liability_from_db.owner.id
        assert liability_from_repo.created_at == liability_from_db.created_at
        assert liability_from_repo.updated_at == liability_from_db.updated_at

    def test_update_liability_domain_through_repo(self, default_account):
        # Arrange: Create an liability domain using the factory
        liability = LiabilityDomainFactory(owner=default_account)
        liability_from_repo = LiabilityRepo.create(liability)
        updated_name = "Updated Liability Domain"

        # Act: Update the liability domain object (before saving)
        liability_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_liability = LiabilityRepo.save(liability_from_repo)

        # Query the database to verify the updated liability record
        liability_from_db = db.session.scalars(
            sa.select(Liability).where(Liability.id == liability_from_repo.id)
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_liability.id == liability_from_db.id
        assert updated_liability.name == liability_from_db.name
        assert updated_liability.created_at == liability_from_db.created_at
        assert updated_liability.updated_at == liability_from_db.updated_at
        # Update_at from updated_liability should be different from the previous liability domain (the one before update)
        assert updated_liability.updated_at != liability_from_repo.updated_at

    def test_get_liability_domain_by_id_through_repo(self, default_account):
        # Arrange: Create an liability domain using the factory
        liability = LiabilityDomainFactory(owner=default_account)
        liability_from_repo = LiabilityRepo.create(liability)

        # Act: Update the liability domain object (before saving)
        liability_get_by_id = LiabilityRepo.get_by_id(liability_from_repo.id)

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert liability_get_by_id.id == liability_from_repo.id
        assert liability_get_by_id.name == liability_from_repo.name

    def test_get_liability_domain_list_through_repo(self, default_account):
        # Arrange: Create an liability domain using the factory
        account_id = default_account.id
        origin_liability_list_length = len(
            LiabilityRepo.get_list(account_id=account_id)
        )

        # Act: Create 5 new liability domains
        for _ in range(5):
            liability = LiabilityDomainFactory(owner=default_account)
            LiabilityRepo.create(liability)

        # Act: Retrieve the updated liability list
        updated_liability_list_length = len(
            LiabilityRepo.get_list(account_id=account_id)
        )

        # Assert: Ensure the list length is increased by 5
        assert updated_liability_list_length == (origin_liability_list_length + 5)

    def test_delete_liability_domain_through_repo(self, default_account):
        # Arrange: Create an liability domain using the factory
        liability = LiabilityDomainFactory(owner=default_account)
        liability_from_repo = LiabilityRepo.create(liability)

        # Act: Delete the liability domain object
        LiabilityRepo.delete_by_id(liability_from_repo.id)

        # Assert: Ensure the liability record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(Liability).where(Liability.id == liability_from_repo.id)
            )
            is None
        )
