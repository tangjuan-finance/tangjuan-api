# from app.domain.entities import IncomeDomain
from app.domain.association import ScenarioIncomeDomain
from tests.unit.factories import IncomeDomainFactory
from decimal import Decimal


class TestIncomeDomainCase:
    def test_create_income_domain():
        # Arrange
        default_max_yearly_growth_rate = Decimal("0.2")
        income = IncomeDomainFactory(
            name="income", max_yearly_growth_rate=default_max_yearly_growth_rate
        )
        max_yearly_growth_rate = Decimal("0.7")
        # Act
        scenario_income = ScenarioIncomeDomain(
            income=income,
            max_yearly_growth_rate=max_yearly_growth_rate,
        )
        # Assert
        assert scenario_income.income.name == "income"
        assert scenario_income.max_yearly_growth_rate != default_max_yearly_growth_rate
        assert scenario_income.max_yearly_growth_rate == max_yearly_growth_rate
