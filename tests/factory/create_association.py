# from app.domain.entities import (
#     AccountDomain,
#     ScenarioDomain,
#     ExpenseDomain,
#     IncomeDomain,
#     HouseDomain,
#     ChildDomain,
#     RiskDomain,
#     AssetDomain,
#     LiabilityDomain,
# )

# from app.domain.associations import (
#     ScenarioExpenseDomain,
#     ScenarioIncomeDomain,
#     ScenarioHouseDomain,
#     ScenarioChildDomain,
#     ScenarioRiskDomain,
#     ScenarioAssetDomain,
#     ScenarioLiabilityDomain,
# )


# def create_scenario_expense(
#     scenario: ScenarioDomain, expense: ExpenseDomain
# ) -> ScenarioExpenseDomain:
#     expense = ExpenseDomainFactory(owner=owner)
#     return ExpenseRepo.create(expense)


# def create_scenario_income(
#     scenario: ScenarioDomain, income: IncomeDomain
# ) -> ScenarioIncomeDomain:
#     income = IncomeDomainFactory(owner=owner)
#     return IncomeRepo.create(income)


# def create_scenario_house(
#     scenario: ScenarioDomain, house: HouseDomain
# ) -> ScenarioHouseDomain:
#     house = HouseDomainFactory(owner=owner)
#     return HouseRepo.create(house)


# def create_scenario_child(
#     parent: AccountDomain, child: ChildDomain
# ) -> ScenarioChildDomain:
#     child = ChildDomainFactory(parent=parent)
#     return ChildRepo.create(child)


# def create_scenario_risk(
#     scenario: ScenarioDomain, risk: RiskDomain
# ) -> ScenarioRiskDomain:
#     risk = RiskDomainFactory(owner=owner)
#     return RiskRepo.create(risk)


# def create_scenario_asset(
#     scenario: ScenarioDomain, asset: AssetDomain
# ) -> ScenarioAssetDomain:
#     asset = AssetDomainFactory(owner=owner)
#     return AssetRepo.create(asset)


# def create_scenario_liability(
#     scenario: ScenarioDomain, liability: LiabilityDomain
# ) -> ScenarioLiabilityDomain:
#     liability = LiabilityDomainFactory(owner=owner)
#     return LiabilityRepo.create(liability)
