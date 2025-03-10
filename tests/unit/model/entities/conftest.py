import pytest
from app import create_app, db
from app.models import Age, User
from tests.conftest import TestConfig


@pytest.fixture(scope="class", autouse=True)
def init_db():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture(scope="class")
def default_user():
    username = "default"
    email = "default@example.com"
    password = "default$ercet"
    about_me = "I am a default user"

    u = User(username=username, email=email, about_me=about_me)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    yield u


def create_age(year):
    age = Age(year=year)
    db.session.add(age)
    db.session.commit()
    return age
