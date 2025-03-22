import pytest
from app.domain.entities import (
    AccountDomain,
    ScenarioDomain,
    ExpenseDomain,
    IncomeDomain,
    HouseDomain,
    ChildDomain,
    RiskDomain,
    AssetDomain,
    LiabilityDomain,
)
from decimal import Decimal
from datetime import datetime, timezone
from nanoid import generate
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="class")
def default_account_domain():
    username = "default"
    email = "default@example.com"
    password = "default$ercet"
    id = generate(size=13)
    password_hash = generate_password_hash(password)
    last_seen = datetime.now(timezone.utc)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    account = AccountDomain(
        username=username,
        email=email,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        password_hash=password_hash,
        last_seen=last_seen,
    )
    yield account


@pytest.fixture(scope="class")
def default_child_domain(default_account_domain):
    name = "Default Child Domain"
    birth_age = 34
    independent_age = 56
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    child = ChildDomain(
        parent=default_account_domain,
        name=name,
        birth_age=birth_age,
        independent_age=independent_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield child


@pytest.fixture(scope="class")
def default_asset_domain(default_account_domain):
    name = "Default Asset Domain"
    amount = 50000
    max_yearly_return_rate = Decimal("0.5")
    min_yearly_return_rate = Decimal("-0.5")
    start_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    asset = AssetDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_return_rate=max_yearly_return_rate,
        min_yearly_return_rate=min_yearly_return_rate,
        start_age=start_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield asset


@pytest.fixture(scope="class")
def default_expense_domain(default_account_domain):
    name = "Default Expense Domain"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
    start_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    expense = ExpenseDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield expense


@pytest.fixture(scope="class")
def default_house_domain(default_account_domain):
    name = "Default House Domain"
    amount = 20000000
    down_payment = 3000000
    interest_rate = Decimal("3")
    loan_term = 40
    purchase_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    house = HouseDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        down_payment=down_payment,
        interest_rate=interest_rate,
        loan_term=loan_term,
        purchase_age=purchase_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield house


@pytest.fixture(scope="class")
def default_income_domain(default_account_domain):
    name = "Default Income Domain"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
    start_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    income = IncomeDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield income


@pytest.fixture(scope="class")
def default_liability_domain(default_account_domain):
    name = "Default Liability Domain"
    principal_amount = 50000
    interest_rate = Decimal("0.5")
    start_age = 20
    end_age = 50
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    liability = LiabilityDomain(
        owner=default_account_domain,
        name=name,
        principal_amount=principal_amount,
        interest_rate=interest_rate,
        start_age=start_age,
        end_age=end_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield liability


@pytest.fixture(scope="class")
def default_risk_domain(default_account_domain):
    name = "Default Risk Domain"
    max_loss = 100000
    min_loss = 50000
    start_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    risk = RiskDomain(
        owner=default_account_domain,
        name=name,
        max_loss=max_loss,
        min_loss=min_loss,
        start_age=start_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield risk


@pytest.fixture(scope="class")
def default_scenario_domain(default_account_domain):
    name = "Default Scenario Domain"
    asset_allocation_percentage = Decimal("0.7")
    retire_age = 20
    id = generate(size=13)
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    scenario = ScenarioDomain(
        owner=default_account_domain,
        name=name,
        asset_allocation_percentage=asset_allocation_percentage,
        retire_age=retire_age,
        id=id,
        created_at=created_at,
        updated_at=updated_at,
    )
    yield scenario
