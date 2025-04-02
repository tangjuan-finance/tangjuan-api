import faker
from tests.unit.factories import AccountDomainFactory
from app.repository.entities import AccountRepo
from app.domain.entities import AccountDomain

faker = faker.Faker()


def create_account() -> AccountDomain:
    """Create a new account."""
    account = AccountDomainFactory()
    return AccountRepo.create(account)
