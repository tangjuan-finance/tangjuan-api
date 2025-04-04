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
        assert hasattr(asset, "end_age")

        assert isinstance(asset.description, str)
        assert isinstance(asset.end_age, int)

    def test_expense_factory_optioanl(self):
        expense = ExpenseDomainFactory(optional=True)

        assert hasattr(expense, "description")
        assert hasattr(expense, "end_age")

        assert isinstance(expense.description, str)
        assert isinstance(expense.end_age, int)

    def test_income_factory_optioanl(self):
        income = IncomeDomainFactory(optional=True)

        assert hasattr(income, "description")
        assert hasattr(income, "end_age")

        assert isinstance(income.description, str)
        assert isinstance(income.end_age, int)

    def test_house_factory_optioanl(self):
        house = HouseDomainFactory(optional=True)

        assert hasattr(house, "description")
        assert hasattr(house, "sale_age")

        assert isinstance(house.description, str)
        assert isinstance(house.sale_age, int)

    def test_child_factory_optioanl(self):
        child = ChildDomainFactory(optional=True)

        assert hasattr(child, "description")
        assert hasattr(child, "independent_age")

        assert isinstance(child.description, str)
        assert isinstance(child.independent_age, int)

    def test_liability_factory_optioanl(self):
        liability = LiabilityDomainFactory(optional=True)

        assert hasattr(liability, "description")

        assert isinstance(liability.description, str)

    def test_risk_factory_optioanl(self):
        risk = RiskDomainFactory(optional=True)

        assert hasattr(risk, "description")
        assert hasattr(risk, "end_age")

        assert isinstance(risk.description, str)
        assert isinstance(risk.end_age, int)

    def test_scenario_factory_optioanl(self):
        scenario = ScenarioDomainFactory(optional=True)

        assert hasattr(scenario, "description")

        assert isinstance(scenario.description, str)
