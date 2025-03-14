from app import db
from app.models import Account


def create_entity(cls, **kwargs):
    entity = cls(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity


def create_account(
    username="alice",
    email="alice@example.com",
    password="bird",
    about_me="Alice likes cute bird.",
):
    u = Account(username=username, email=email, about_me=about_me)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u
