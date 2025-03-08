from app import db
from app.models import User, Salary, Expense


def create_entity(cls, **kwargs):
    entity = cls(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity


def create_user(
    username="alice",
    email="alice@example.com",
    password="bird",
    about_me="Alice likes cute bird.",
):
    u = User(username=username, email=email, about_me=about_me)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


def create_salary(owner, start_year, name, amount=50000):
    salary = create_entity(
        Salary, owner=owner, start_year=start_year, name=name, amount=amount
    )
    return salary


def create_expense(owner, start_year, name, amount=50000):
    expense = create_entity(
        Expense, owner=owner, start_year=start_year, name=name, amount=amount
    )
    return expense
