import pytest
from typing import Generator
from app.domain.entities import ScenarioDomain
from .factories import create_scenario


@pytest.fixture(scope="module")
def default_scenario(default_account) -> Generator[ScenarioDomain, None, None]:
    """Provides a default scenario for scenario resource tests."""
    yield create_scenario(default_account)
