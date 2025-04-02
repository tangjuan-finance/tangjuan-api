# from app.domain.entities import IncomeDomain
from app.domain.associations import ScenarioIncomeDomain
from tests.factory import IncomeDomainFactory
from decimal import Decimal
from datetime import datetime, timezone


class TestIncomeDomainCase:
    def test_create_scenario_income_domain(self, default_scenario_domain):
        # Arrange
        name = "income for scenario"

        default_max_yearly_growth_rate = Decimal("0.2")
        income = IncomeDomainFactory(
            name=name, max_yearly_growth_rate=default_max_yearly_growth_rate
        )
        max_yearly_growth_rate = Decimal("0.7")
        # Act
        scenario_income = ScenarioIncomeDomain(
            scenario_id=default_scenario_domain.id,
            income_id=income.id,
            max_yearly_growth_rate=max_yearly_growth_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_income.scenario_id == default_scenario_domain.id
        assert scenario_income.income_id == income.id
        assert scenario_income.max_yearly_growth_rate != default_max_yearly_growth_rate
        assert scenario_income.max_yearly_growth_rate == max_yearly_growth_rate
