import pytest
from app import create_app, db
from app.infrastructure.models import (
    Account,
    Scenario,
    Expense,
    Income,
    House,
    Child,
    Risk,
    Asset,
    Liability,
)
from tests.conftest import TestConfig
from .factories import create_entity
from werkzeug.security import generate_password_hash


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
def default_account_domain():
    name = "default"
    email = "default@example.com"
    password = "default$ercet"
    password_hash = generate_password_hash(password)

    u = Account(name=name, email=email, password_hash=password_hash)
    db.session.add(u)
    db.session.commit()
    yield u


@pytest.fixture(scope="class")
def default_scenario(default_account_domain):
    name = "Default Scenario"
    asset_allocation_percentage = 0.7
    retire_age = 20

    scenario = create_entity(
        Scenario,
        owner=default_account_domain,
        name=name,
        asset_allocation_percentage=asset_allocation_percentage,
        retire_age=retire_age,
    )
    yield scenario


@pytest.fixture(scope="class")
def default_risk(default_account_domain):
    name = "Default Risk"
    max_loss = 100000
    min_loss = 50000
    start_age = 20
    end_age = 30

    risk = create_entity(
        Risk,
        owner=default_account_domain,
        name=name,
        start_age=start_age,
        end_age=end_age,
        max_loss=max_loss,
        min_loss=min_loss,
    )
    yield risk


@pytest.fixture(scope="class")
def default_liability(default_account_domain):
    name = "Default Liability"
    principal_amount = 50000
    interest_rate = 0.5
    start_age = 20
    end_age = 50

    liability = create_entity(
        Liability,
        owner=default_account_domain,
        name=name,
        principal_amount=principal_amount,
        interest_rate=interest_rate,
        start_age=start_age,
        end_age=end_age,
    )
    yield liability


@pytest.fixture(scope="class")
def default_income(default_account_domain):
    name = "Default Income"
    amount = 50000
    max_yearly_growth_rate = 0.5
    min_yearly_growth_rate = -0.5
    start_age = 20
    end_age = 65

    income = create_entity(
        Income,
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
        end_age=end_age,
    )
    yield income


@pytest.fixture(scope="class")
def default_house(default_account_domain):
    name = "Default House"
    amount = 20000000
    down_payment = 3000000
    interest_rate = 3.0
    loan_term = 40
    purchase_age = 20
    sale_age = 40

    house = create_entity(
        House,
        owner=default_account_domain,
        name=name,
        amount=amount,
        down_payment=down_payment,
        interest_rate=interest_rate,
        loan_term=loan_term,
        purchase_age=purchase_age,
        sale_age=sale_age,
    )
    yield house


@pytest.fixture(scope="class")
def default_expense(default_account_domain):
    name = "Default Expense"
    amount = 50000
    max_yearly_growth_rate = 0.5
    min_yearly_growth_rate = -0.5
    start_age = 20
    end_age = 100

    expense = create_entity(
        Expense,
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
        end_age=end_age,
    )
    yield expense


@pytest.fixture(scope="class")
def default_child(default_account_domain):
    name = "Default Child"
    birth_age = 34
    independent_age = 56

    child = create_entity(
        Child,
        parent=default_account_domain,
        name=name,
        birth_age=birth_age,
        independent_age=independent_age,
    )
    yield child


@pytest.fixture(scope="class")
def default_asset(default_account_domain):
    name = "Default Asset"
    amount = 50000
    max_yearly_return_rate = 0.5
    min_yearly_return_rate = -0.5
    start_age = 20
    end_age = 100

    asset = create_entity(
        Asset,
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_return_rate=max_yearly_return_rate,
        min_yearly_return_rate=min_yearly_return_rate,
        start_age=start_age,
        end_age=end_age,
    )
    yield asset
