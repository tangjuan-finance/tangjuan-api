import pytest
from app import create_app, db
from typing import Generator
from tests.conftest import TestConfig
from app.domain.entities import AccountDomain, ScenarioDomain
from .factories import create_account, create_scenario


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


@pytest.fixture(scope="module")
def default_scenario(default_account) -> Generator[ScenarioDomain, None, None]:
    """Provides a default scenario for scenario resource tests."""
    yield create_scenario(default_account)
