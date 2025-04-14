from app.domain.entities import AccountDomain
from tests.factory import (
    AccountDomainFactory,
    ScenarioDomainFactory,
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)
from app.repository.entities import (
    AccountRepo,
    ScenarioRepo,
    ExpenseRepo,
    IncomeRepo,
    HouseRepo,
    ChildRepo,
    RiskRepo,
    AssetRepo,
    LiabilityRepo,
)


def create_account(*args, **kwargs) -> AccountDomain:
    """Create a new account."""
    account = AccountDomainFactory(*args, **kwargs)
    return AccountRepo.create(account)


def create_scenario(*args, **kwargs):
    scenario = ScenarioDomainFactory(*args, **kwargs)
    return ScenarioRepo.create(scenario)


def create_expense(*args, **kwargs):
    expense = ExpenseDomainFactory(*args, **kwargs)
    return ExpenseRepo.create(expense)


def create_income(*args, **kwargs):
    income = IncomeDomainFactory(*args, **kwargs)
    return IncomeRepo.create(income)


def create_house(*args, **kwargs):
    house = HouseDomainFactory(*args, **kwargs)
    return HouseRepo.create(house)


def create_child(*args, **kwargs):
    child = ChildDomainFactory(*args, **kwargs)
    return ChildRepo.create(child)


def create_risk(*args, **kwargs):
    risk = RiskDomainFactory(*args, **kwargs)
    return RiskRepo.create(risk)


def create_asset(*args, **kwargs):
    asset = AssetDomainFactory(*args, **kwargs)
    return AssetRepo.create(asset)


def create_liability(*args, **kwargs):
    liability = LiabilityDomainFactory(*args, **kwargs)
    return LiabilityRepo.create(liability)
