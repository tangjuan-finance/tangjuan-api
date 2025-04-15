from tests.factory import (
    ChildDomainFactory,
    AssetDomainFactory,
    ExpenseDomainFactory,
    HouseDomainFactory,
    IncomeDomainFactory,
    LiabilityDomainFactory,
    RiskDomainFactory,
    ScenarioDomainFactory,
)


class TestDomainFactory:
    def test_asset_factory_optioanl(self):
        asset = AssetDomainFactory(optional=True)

        assert hasattr(asset, "description")

        assert isinstance(asset.description, str)

    def test_expense_factory_optioanl(self):
        expense = ExpenseDomainFactory(optional=True)

        assert hasattr(expense, "description")

        assert isinstance(expense.description, str)

    def test_income_factory_optioanl(self):
        income = IncomeDomainFactory(optional=True)

        assert hasattr(income, "description")

        assert isinstance(income.description, str)

    def test_house_factory_optioanl(self):
        house = HouseDomainFactory(optional=True)

        assert hasattr(house, "description")

        assert isinstance(house.description, str)

    def test_child_factory_optioanl(self):
        child = ChildDomainFactory(optional=True)

        assert hasattr(child, "description")

        assert isinstance(child.description, str)

    def test_liability_factory_optioanl(self):
        liability = LiabilityDomainFactory(optional=True)

        assert hasattr(liability, "description")

        assert isinstance(liability.description, str)

    def test_risk_factory_optioanl(self):
        risk = RiskDomainFactory(optional=True)

        assert hasattr(risk, "description")

        assert isinstance(risk.description, str)

    def test_scenario_factory_optioanl(self):
        scenario = ScenarioDomainFactory(optional=True)

        assert hasattr(scenario, "description")

        assert isinstance(scenario.description, str)
