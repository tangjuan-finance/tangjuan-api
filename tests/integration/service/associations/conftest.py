import pytest
from typing import Generator
from app.domain.entities import (
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
    create_scenario,
    create_expense,
    create_income,
    create_house,
    create_child,
    create_risk,
    create_asset,
    create_liability,
)


@pytest.fixture(scope="function")
def default_scenario_id(default_account) -> Generator[ScenarioDomain, None, None]:
    """Provides a default scenario for scenario resource tests."""
    yield create_scenario(default_account).id


@pytest.fixture(scope="function")
def default_expense_id(default_account) -> Generator[ExpenseDomain, None, None]:
    """Provides a default expense for expense resource tests."""
    yield create_expense(default_account).id


@pytest.fixture(scope="function")
def default_income_id(default_account) -> Generator[IncomeDomain, None, None]:
    """Provides a default income for income resource tests."""
    yield create_income(default_account).id


@pytest.fixture(scope="function")
def default_house_id(default_account) -> Generator[HouseDomain, None, None]:
    """Provides a default house for house resource tests."""
    yield create_house(default_account).id


@pytest.fixture(scope="function")
def default_child_id(default_account) -> Generator[ChildDomain, None, None]:
    """Provides a default child for child resource tests."""
    yield create_child(default_account).id


@pytest.fixture(scope="function")
def default_risk_id(default_account) -> Generator[RiskDomain, None, None]:
    """Provides a default risk for risk resource tests."""
    yield create_risk(default_account).id


@pytest.fixture(scope="function")
def default_asset_id(default_account) -> Generator[AssetDomain, None, None]:
    """Provides a default asset for asset resource tests."""
    yield create_asset(default_account).id


@pytest.fixture(scope="function")
def default_liability_id(default_account) -> Generator[LiabilityDomain, None, None]:
    """Provides a default liability for liability resource tests."""
    yield create_liability(default_account).id
