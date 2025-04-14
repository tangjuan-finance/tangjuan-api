from app import db
from app.infrastructure.models import Account
from werkzeug.security import generate_password_hash
from tests.factory import create_fake_id


def create_entity(cls, **kwargs):
    entity = cls(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity


def create_account(
    id=create_fake_id(),
    name="alice",
    email="alice@example.com",
    password="bird",
):
    password_hash = generate_password_hash(password)

    u = Account(id=id, name=name, email=email, password_hash=password_hash)
    db.session.add(u)
    db.session.commit()
    return u
