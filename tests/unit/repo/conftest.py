import pytest
from app import create_app, db
from tests.conftest import TestConfig


# Using Factory to generate domain object, so each object should be indenpendent in database record
@pytest.fixture(scope="module", autouse=True)
def init_db():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()
