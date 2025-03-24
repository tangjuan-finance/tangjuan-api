from app.repository.entities import AccountRepo
from app.infrastructure.models.entities import Account
from tests.unit.factories import AccountDomainFactory
import sqlalchemy as sa
from app import db


class TestAccountRepoCase:
    def test_create_account_domain_through_repo(self):
        # Arrange: Create an account domain using the factory
        account = AccountDomainFactory()

        # Act: Save the account domain using the repo and return the saved entity
        account_from_repo = AccountRepo.create(account)
        account_from_db = db.session.scalar(
            sa.select(Account).where(Account.id == account.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert account_from_repo.id == account_from_db.id
        assert account_from_repo.username == account_from_db.username
        assert account_from_repo.email == account_from_db.email
        assert account_from_repo.password_hash == account_from_db.password_hash
        assert account_from_repo.created_at == account_from_db.created_at
        assert account_from_repo.updated_at == account_from_db.updated_at

    def test_update_account_domain_through_repo(self):
        # Arrange: Create an account domain using the factory
        account = AccountDomainFactory()
        account_from_repo = AccountRepo.create(account)
        updated_username = "Updated Account Domain"

        # Act: Update the account domain object (before saving)
        account_from_repo.username = updated_username

        # Save the updated object through the repository and get the result
        updated_account = AccountRepo.save(account_from_repo)

        # Query the database to verify the updated account record
        account_from_db = db.session.scalar(
            sa.select(Account).where(Account.id == account_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_account.id == account_from_db.id
        assert updated_account.username == account_from_db.username
        assert updated_account.created_at == account_from_db.created_at
        assert updated_account.updated_at != account_from_db.updated_at

    def test_get_account_domain_by_id_through_repo(self):
        # Arrange: Create an account domain using the factory
        account = AccountDomainFactory()
        AccountRepo.create(account)

        # Act: Update the account domain object (before saving)
        account_get_by_id = AccountRepo.get_by_id(account.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert account_get_by_id.id == account.id
        assert account_get_by_id.username == account.username

    def test_get_account_domain_list_through_repo(self):
        # Arrange: Create an account domain using the factory
        origin_account_list_length = len(AccountRepo.get_list())

        # Act: Create 5 new account domains
        for _ in range(5):
            account = AccountDomainFactory()
            AccountRepo.create(account)

        # Assert: Ensure the list length is increased by 5
        updated_account_list_length = len(AccountRepo.get_list())
        assert updated_account_list_length == (origin_account_list_length + 5)

    def test_delete_account_domain_through_repo(self):
        # Arrange: Create an account domain using the factory
        account = AccountDomainFactory()
        account_from_repo = AccountRepo.create(account)

        # Act: Delete the account domain object
        AccountRepo.delete(account_from_repo)

        # Assert: Ensure the account record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(Account).where(Account.id == account_from_repo.id)
            )
            is None
        )
