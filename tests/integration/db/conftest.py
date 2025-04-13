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
    ChildSavingPlan,
    ChildSavingAmountEntry,
)
from tests.conftest import TestConfig
from .factories import create_entity
from werkzeug.security import generate_password_hash
from decimal import Decimal


# @pytest.fixture(scope="class", autouse=True)
# Restart db every function to ensure each session not affect each other
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


@pytest.fixture(scope="function")
def default_account_domain():
    name = "default"
    email = "default@example.com"
    password = "default$ercet"
    password_hash = generate_password_hash(password)

    u = Account(name=name, email=email, password_hash=password_hash)
    db.session.add(u)
    db.session.commit()
    yield u


@pytest.fixture(scope="function")
def default_scenario(default_account_domain):
    name = "Default Scenario"
    asset_allocation_percentage = Decimal("0.7")
    retire_age = 20

    scenario = create_entity(
        Scenario,
        owner=default_account_domain,
        name=name,
        asset_allocation_percentage=asset_allocation_percentage,
        retire_age=retire_age,
    )
    yield scenario


@pytest.fixture(scope="function")
def default_risk(default_account_domain):
    name = "Default Risk"
    amount = 100000
    probability = Decimal("0.2")
    start_age = 20
    end_age = 30

    risk = create_entity(
        Risk,
        owner=default_account_domain,
        name=name,
        start_age=start_age,
        end_age=end_age,
        amount=amount,
        probability=probability,
    )
    yield risk


@pytest.fixture(scope="function")
def default_liability(default_account_domain):
    name = "Default Liability"
    principal_amount = 50000
    interest_rate = Decimal("0.5")
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


@pytest.fixture(scope="function")
def default_income(default_account_domain):
    name = "Default Income"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
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


@pytest.fixture(scope="function")
def default_house(default_account_domain):
    name = "Default House"
    amount = 20000000
    down_payment = 3000000
    interest_rate = Decimal("3.0")
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


@pytest.fixture(scope="function")
def default_expense(default_account_domain):
    name = "Default Expense"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
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


@pytest.fixture(scope="function")
def default_child(default_account_domain, default_child_saving_plan):
    name = "Default Child"
    birth_age = 34
    independent_age = 56

    child = create_entity(
        Child,
        parent=default_account_domain,
        name=name,
        birth_age=birth_age,
        independent_age=independent_age,
        child_saving_plan=default_child_saving_plan,
    )
    yield child


@pytest.fixture(scope="function")
def default_child_saving_plan():
    name = "Default Child Saving Plan"

    child_saving_plan = create_entity(
        ChildSavingPlan,
        name=name,
    )
    yield child_saving_plan


@pytest.fixture(scope="function")
def default_child_saving_amount_entry(default_child_saving_plan):
    age = 15
    amount = 200000

    child_saving_amount_entry = create_entity(
        ChildSavingAmountEntry,
        age=age,
        amount=amount,
        child_saving_plan=default_child_saving_plan,
    )
    yield child_saving_amount_entry


@pytest.fixture(scope="function")
def default_asset(default_account_domain):
    name = "Default Asset"
    amount = 50000
    max_yearly_return_rate = Decimal("0.5")
    min_yearly_return_rate = Decimal("-0.5")
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
