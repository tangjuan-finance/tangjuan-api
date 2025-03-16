from app import db
from app.infrastructure.models import Account


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
    u = Account(username=username, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u
