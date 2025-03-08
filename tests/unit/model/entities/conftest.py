import pytest
from app import create_app, db
from app.models import Age
from tests.conftest import TestConfig


@pytest.fixture(scope="function", autouse=True)
def init_db():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


def create_age(year):
    age = Age(year=year)
    db.session.add(age)
    db.session.commit()
    return age
