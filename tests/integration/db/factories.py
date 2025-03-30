from app import db
from app.infrastructure.models import Account
from werkzeug.security import generate_password_hash


def create_entity(cls, **kwargs):
    entity = cls(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity


def create_account(
    username="alice",
    email="alice@example.com",
    password="bird",
):
    password_hash = generate_password_hash(password)

    u = Account(username=username, email=email, password_hash=password_hash)
    db.session.add(u)
    db.session.commit()
    return u
