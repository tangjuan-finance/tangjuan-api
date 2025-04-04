import pytest
from typing import Generator


@pytest.fixture(scope="function")
def default_scenario_id(default_scenario) -> Generator[str, None, None]:
    """Provides a default scenario for scenario resource tests."""
    yield default_scenario.id


@pytest.fixture(scope="function")
def default_expense_id(default_expense) -> Generator[str, None, None]:
    """Provides a default expense for expense resource tests."""
    yield default_expense.id


@pytest.fixture(scope="function")
def default_income_id(default_income) -> Generator[str, None, None]:
    """Provides a default income for income resource tests."""
    yield default_income.id


@pytest.fixture(scope="function")
def default_house_id(default_house) -> Generator[str, None, None]:
    """Provides a default house for house resource tests."""
    yield default_house.id


@pytest.fixture(scope="function")
def default_child_id(default_child) -> Generator[str, None, None]:
    """Provides a default child for child resource tests."""
    yield default_child.id


@pytest.fixture(scope="function")
def default_risk_id(default_risk) -> Generator[str, None, None]:
    """Provides a default risk for risk resource tests."""
    yield default_risk.id


@pytest.fixture(scope="function")
def default_asset_id(default_asset) -> Generator[str, None, None]:
    """Provides a default asset for asset resource tests."""
    yield default_asset.id


@pytest.fixture(scope="function")
def default_liability_id(default_liability) -> Generator[str, None, None]:
    """Provides a default liability for liability resource tests."""
    yield default_liability.id
