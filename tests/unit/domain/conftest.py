import pytest
from app.domain.entity import (
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


@pytest.fixture(scope="class")
def default_account_domain():
    username = "default"
    email = "default@example.com"
    password = "default$ercet"

    account = AccountDomain(username=username, email=email)
    account.set_password(password)
    yield account


@pytest.fixture(scope="class")
def default_child_domain(default_account_domain):
    name = "Default Child Domain"
    birth_age = 34
    independent_age = 56

    child = ChildDomain(
        owner=default_account_domain,
        name=name,
        birth_age=birth_age,
        independent_age=independent_age,
    )
    yield child


@pytest.fixture(scope="class")
def default_asset_domain(default_account_domain):
    name = "Default Asset Domain"
    amount = 50000
    max_yearly_return_rate = Decimal("0.5")
    min_yearly_return_rate = Decimal("-0.5")
    start_age = 20

    asset = AssetDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_return_rate=max_yearly_return_rate,
        min_yearly_return_rate=min_yearly_return_rate,
        start_age=start_age,
    )
    yield asset


@pytest.fixture(scope="class")
def default_expense_domain(default_account_domain):
    name = "Default Expense Domain"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
    start_age = 20

    expense = ExpenseDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
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

    house = HouseDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        down_payment=down_payment,
        interest_rate=interest_rate,
        loan_term=loan_term,
        purchase_age=purchase_age,
    )
    yield house


@pytest.fixture(scope="class")
def default_income_domain(default_account_domain):
    name = "Default Income Domain"
    amount = 50000
    max_yearly_growth_rate = Decimal("0.5")
    min_yearly_growth_rate = Decimal("-0.5")
    start_age = 20

    income = IncomeDomain(
        owner=default_account_domain,
        name=name,
        amount=amount,
        max_yearly_growth_rate=max_yearly_growth_rate,
        min_yearly_growth_rate=min_yearly_growth_rate,
        start_age=start_age,
    )
    yield income


@pytest.fixture(scope="class")
def default_liability_domain(default_account_domain):
    name = "Default Liability Domain"
    principal_amount = 50000
    interest_rate = Decimal("0.5")
    start_age = 20
    end_age = 50

    liability = LiabilityDomain(
        owner=default_account_domain,
        name=name,
        principal_amount=principal_amount,
        interest_rate=interest_rate,
        start_age=start_age,
        end_age=end_age,
    )
    yield liability


@pytest.fixture(scope="class")
def default_risk_domain(default_account_domain):
    name = "Default Risk Domain"
    max_loss = 100000
    min_loss = 50000
    start_age = 20

    risk = RiskDomain(
        owner=default_account_domain,
        name=name,
        max_loss=max_loss,
        min_loss=min_loss,
        start_age=start_age,
    )
    yield risk


@pytest.fixture(scope="class")
def default_scenario_domain(default_account_domain):
    name = "Default Scenario Domain"
    asset_allocation_percentage = Decimal("0.7")
    retire_age = 20

    scenario = ScenarioDomain(
        owner=default_account_domain,
        name=name,
        asset_allocation_percentage=asset_allocation_percentage,
        retire_age=retire_age,
    )
    yield scenario
