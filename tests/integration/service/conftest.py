import pytest
from app import create_app, db
from typing import Generator
from tests.conftest import TestConfig
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
from tests.factory import (
    create_account,
    create_scenario,
    create_expense,
    create_income,
    create_house,
    create_child,
    create_risk,
    create_asset,
    create_liability,
)


@pytest.fixture(scope="module", autouse=True)
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


@pytest.fixture(scope="module")
def default_account() -> Generator[AccountDomain, None, None]:
    """Provides a default account used as an owner in tests."""
    yield create_account()


@pytest.fixture(scope="function")
def default_scenario(default_account) -> Generator[ScenarioDomain, None, None]:
    """Provides a default scenario for scenario resource tests."""
    yield create_scenario(default_account)


@pytest.fixture(scope="function")
def default_expense(default_account) -> Generator[ExpenseDomain, None, None]:
    """Provides a default expense for expense resource tests."""
    yield create_expense(default_account)


@pytest.fixture(scope="function")
def default_income(default_account) -> Generator[IncomeDomain, None, None]:
    """Provides a default income for income resource tests."""
    yield create_income(default_account)


@pytest.fixture(scope="function")
def default_house(default_account) -> Generator[HouseDomain, None, None]:
    """Provides a default house for house resource tests."""
    yield create_house(default_account)


@pytest.fixture(scope="function")
def default_child(default_account) -> Generator[ChildDomain, None, None]:
    """Provides a default child for child resource tests."""
    yield create_child(default_account)


@pytest.fixture(scope="function")
def default_risk(default_account) -> Generator[RiskDomain, None, None]:
    """Provides a default risk for risk resource tests."""
    yield create_risk(default_account)


@pytest.fixture(scope="function")
def default_asset(default_account) -> Generator[AssetDomain, None, None]:
    """Provides a default asset for asset resource tests."""
    yield create_asset(default_account)


@pytest.fixture(scope="function")
def default_liability(default_account) -> Generator[LiabilityDomain, None, None]:
    """Provides a default liability for liability resource tests."""
    yield create_liability(default_account)
