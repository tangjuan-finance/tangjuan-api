import pytest
from app import create_app, db
from typing import Generator
from tests.conftest import TestConfig
from tests.factory import (
    AccountDomainFactory,
    ScenarioDomainFactory,
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)
from app.repository.entities import (
    AccountRepo,
    ScenarioRepo,
    ExpenseRepo,
    IncomeRepo,
    HouseRepo,
    ChildRepo,
    RiskRepo,
    AssetRepo,
    LiabilityRepo,
)
from app.domain.entities import (
    AccountDomain,
    ScenarioDomain,
    ExpenseDomain,
    IncomeDomain,
    HouseDomain,
    ChildDomain,
    RiskDomain,
    AssetDomain,
    LiabilityDomain,
)


# Using Factory to generate domain object, so each object should be indenpendent in database record
@pytest.fixture(scope="function", autouse=True)
def init_db():
    """Initialize and clean up the database for testing."""
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture(scope="function")
def default_account() -> Generator[AccountDomain, None, None]:
    """Provides a default account used as an owner in tests."""
    account = AccountDomainFactory()
    yield AccountRepo.create(account)


@pytest.fixture(scope="function")
def new_scenario(default_account) -> Generator[ScenarioDomain, None, None]:
    """Creates a new scenario associated with the default account."""
    scenario = ScenarioDomainFactory(owner=default_account)
    yield ScenarioRepo.create(scenario)


@pytest.fixture(scope="function")
def new_expense(default_account) -> Generator[ExpenseDomain, None, None]:
    """Creates a new expense associated with the default account."""
    expense = ExpenseDomainFactory(owner=default_account)
    yield ExpenseRepo.create(expense)


@pytest.fixture(scope="function")
def new_income(default_account) -> Generator[IncomeDomain, None, None]:
    """Creates a new income associated with the default account."""
    income = IncomeDomainFactory(owner=default_account)
    yield IncomeRepo.create(income)


@pytest.fixture(scope="function")
def new_house(default_account) -> Generator[HouseDomain, None, None]:
    """Creates a new house associated with the default account."""
    house = HouseDomainFactory(owner=default_account)
    yield HouseRepo.create(house)


@pytest.fixture(scope="function")
def new_child(default_account) -> Generator[ChildDomain, None, None]:
    """Creates a new child associated with the default account."""
    child = ChildDomainFactory(parent=default_account)
    yield ChildRepo.create(child)


@pytest.fixture(scope="function")
def new_risk(default_account) -> Generator[RiskDomain, None, None]:
    """Creates a new risk associated with the default account."""
    risk = RiskDomainFactory(owner=default_account)
    yield RiskRepo.create(risk)


@pytest.fixture(scope="function")
def new_asset(default_account) -> Generator[AssetDomain, None, None]:
    """Creates a new asset associated with the default account."""
    asset = AssetDomainFactory(owner=default_account)
    yield AssetRepo.create(asset)


@pytest.fixture(scope="function")
def new_liability(default_account) -> Generator[LiabilityDomain, None, None]:
    """Creates a new liability associated with the default account."""
    liability = LiabilityDomainFactory(owner=default_account)
    yield LiabilityRepo.create(liability)
