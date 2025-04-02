import faker
from tests.unit.factories import ScenarioDomainFactory
from app.repository.entities import ScenarioRepo
from app.domain.entities import ScenarioDomain, AccountDomain

faker = faker.Faker()


def create_scenario(owner: AccountDomain) -> ScenarioDomain:
    """Create a new scenario."""
    scenario = ScenarioDomainFactory(owner=owner)
    return ScenarioRepo.create(scenario)
