from app.repository.entities import IncomeRepo
from app.infrastructure.models.entities import Income
from tests.unit.factories import IncomeDomainFactory
import sqlalchemy as sa
from app import db


class TestIncomeRepoCase:
    def test_create_income_domain_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        income = IncomeDomainFactory(owner=default_account)

        # Act: Save the income domain using the repo and return the saved entity
        income_from_repo = IncomeRepo.create(income)
        income_from_db = db.session.scalars(
            sa.select(Income).where(Income.id == income_from_repo.id)
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert income_from_repo.id == income_from_db.id
        assert income_from_repo.name == income_from_db.name
        assert income_from_repo.amount == income_from_db.amount
        assert (
            income_from_repo.max_yearly_growth_rate
            == income_from_db.max_yearly_growth_rate
        )
        assert (
            income_from_repo.min_yearly_growth_rate
            == income_from_db.min_yearly_growth_rate
        )
        assert income_from_repo.start_age == income_from_db.start_age
        assert income_from_repo.owner.id == income_from_db.owner.id
        assert income_from_repo.created_at == income_from_db.created_at
        assert income_from_repo.updated_at == income_from_db.updated_at

    def test_update_income_domain_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        income = IncomeDomainFactory(owner=default_account)
        income_from_repo = IncomeRepo.create(income)
        updated_name = "Updated Income Domain"

        # Act: Update the income domain object (before saving)
        income_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_income = IncomeRepo.save(income_from_repo)

        # Query the database to verify the updated income record
        income_from_db = db.session.scalars(
            sa.select(Income).where(Income.id == income_from_repo.id)
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_income.id == income_from_db.id
        assert updated_income.name == income_from_db.name
        assert updated_income.created_at == income_from_db.created_at
        assert updated_income.updated_at == income_from_db.updated_at
        # Update_at from updated_income should be different from the previous income domain (the one before update)
        assert updated_income.updated_at != income_from_repo.updated_at

    def test_get_income_domain_by_id_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        income = IncomeDomainFactory(owner=default_account)
        income_from_repo = IncomeRepo.create(income)

        # Act: Update the income domain object (before saving)
        income_get_by_id = IncomeRepo.get_by_id(income_from_repo.id)

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert income_get_by_id.id == income_from_repo.id
        assert income_get_by_id.name == income_from_repo.name

    def test_get_income_domain_list_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        account_id = default_account.id
        origin_income_list_length = len(IncomeRepo.get_list(account_id=account_id))

        # Act: Create 5 new income domains
        for _ in range(5):
            income = IncomeDomainFactory(owner=default_account)
            IncomeRepo.create(income)

        # Act: Retrieve the updated income list
        updated_income_list_length = len(IncomeRepo.get_list(account_id=account_id))

        # Assert: Ensure the list length is increased by 5
        assert updated_income_list_length == (origin_income_list_length + 5)

    def test_delete_income_domain_through_repo(self, default_account):
        # Arrange: Create an income domain using the factory
        income = IncomeDomainFactory(owner=default_account)
        income_from_repo = IncomeRepo.create(income)

        # Act: Delete the income domain object
        IncomeRepo.delete_by_id(income_from_repo.id)

        # Assert: Ensure the income record is deleted from the database
        assert (
            db.session.scalar(sa.select(Income).where(Income.id == income_from_repo.id))
            is None
        )
