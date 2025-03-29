from app.domain.entities import AccountDomain
from tests.unit.factories import (
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
    ScenarioRepo,
    ExpenseRepo,
    IncomeRepo,
    HouseRepo,
    ChildRepo,
    RiskRepo,
    AssetRepo,
    LiabilityRepo,
)


def create_scenario(owner: AccountDomain):
    scenario = ScenarioDomainFactory(owner=owner)
    return ScenarioRepo.create(scenario)


def create_expense(owner: AccountDomain):
    expense = ExpenseDomainFactory(owner=owner)
    return ExpenseRepo.create(expense)


def create_income(owner: AccountDomain):
    income = IncomeDomainFactory(owner=owner)
    return IncomeRepo.create(income)


def create_house(owner: AccountDomain):
    house = HouseDomainFactory(owner=owner)
    return HouseRepo.create(house)


def create_child(parent: AccountDomain):
    child = ChildDomainFactory(parent=parent)
    return ChildRepo.create(child)


def create_risk(owner: AccountDomain):
    risk = RiskDomainFactory(owner=owner)
    return RiskRepo.create(risk)


def create_asset(owner: AccountDomain):
    asset = AssetDomainFactory(owner=owner)
    return AssetRepo.create(asset)


def create_liability(owner: AccountDomain):
    liability = LiabilityDomainFactory(owner=owner)
    return LiabilityRepo.create(liability)
