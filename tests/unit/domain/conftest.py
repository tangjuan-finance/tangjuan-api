import pytest
from tests.factory.domain_factory import (
    AccountDomainFactory,
    ScenarioDomainFactory,
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)


@pytest.fixture(scope="function")
def default_account_domain():
    yield AccountDomainFactory()


@pytest.fixture(scope="function")
def default_child_domain(default_account_domain):
    yield ChildDomainFactory(parent=default_account_domain)


@pytest.fixture(scope="function")
def default_child_saving_plan_domain(default_account_domain):
    yield ChildSavingPlanDomainFactory(owner_id=default_account_domain.id)


@pytest.fixture(scope="function")
def default_child_saving_amount_entry_domain():
    yield ChildSavingAmountEntryDomainFactory()


@pytest.fixture(scope="function")
def default_asset_domain(default_account_domain):
    yield AssetDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_expense_domain(default_account_domain):
    yield ExpenseDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_house_domain(default_account_domain):
    yield HouseDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_income_domain(default_account_domain):
    yield IncomeDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_liability_domain(default_account_domain):
    yield LiabilityDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_risk_domain(default_account_domain):
    yield RiskDomainFactory(owner=default_account_domain)


@pytest.fixture(scope="function")
def default_scenario_domain(default_account_domain):
    yield ScenarioDomainFactory(owner=default_account_domain)
