from app.domain.associations import (
    ScenarioExpenseDomain,
    ScenarioIncomeDomain,
    ScenarioHouseDomain,
    ScenarioChildDomain,
    ScenarioRiskDomain,
    ScenarioAssetDomain,
    ScenarioLiabilityDomain,
)

from tests.factory import (
    ScenarioExpenseDomainFactory,
    ScenarioIncomeDomainFactory,
    ScenarioHouseDomainFactory,
    ScenarioChildDomainFactory,
    ScenarioRiskDomainFactory,
    ScenarioAssetDomainFactory,
    ScenarioLiabilityDomainFactory,
)

from app.repository.associations import (
    ScenarioExpenseRepo,
    ScenarioIncomeRepo,
    ScenarioHouseRepo,
    ScenarioChildRepo,
    ScenarioRiskRepo,
    ScenarioAssetRepo,
    ScenarioLiabilityRepo,
)


def create_scenario_expense(scenario_id: str, expense_id: str) -> ScenarioExpenseDomain:
    assoc = ScenarioExpenseDomainFactory(
        optional=True, scenario_id=scenario_id, expense_id=expense_id
    )
    return ScenarioExpenseRepo.create(assoc)


def create_scenario_income(scenario_id: str, income_id: str) -> ScenarioIncomeDomain:
    assoc = ScenarioIncomeDomainFactory(
        optional=True, scenario_id=scenario_id, income_id=income_id
    )
    return ScenarioIncomeRepo.create(assoc)


def create_scenario_house(scenario_id: str, house_id: str) -> ScenarioHouseDomain:
    assoc = ScenarioHouseDomainFactory(
        optional=True, scenario_id=scenario_id, house_id=house_id
    )
    return ScenarioHouseRepo.create(assoc)


def create_scenario_child(scenario_id: str, child_id: str) -> ScenarioChildDomain:
    assoc = ScenarioChildDomainFactory(
        optional=True, scenario_id=scenario_id, child_id=child_id
    )
    return ScenarioChildRepo.create(assoc)


def create_scenario_risk(scenario_id: str, risk_id: str) -> ScenarioRiskDomain:
    assoc = ScenarioRiskDomainFactory(
        optional=True, scenario_id=scenario_id, risk_id=risk_id
    )
    return ScenarioRiskRepo.create(assoc)


def create_scenario_asset(scenario_id: str, asset_id: str) -> ScenarioAssetDomain:
    assoc = ScenarioAssetDomainFactory(
        optional=True, scenario_id=scenario_id, asset_id=asset_id
    )
    return ScenarioAssetRepo.create(assoc)


def create_scenario_liability(
    scenario_id: str, liability_id: str
) -> ScenarioLiabilityDomain:
    assoc = ScenarioLiabilityDomainFactory(
        optional=True, scenario_id=scenario_id, liability_id=liability_id
    )
    return ScenarioLiabilityRepo.create(assoc)
