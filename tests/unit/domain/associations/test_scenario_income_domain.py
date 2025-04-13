# from app.domain.entities import IncomeDomain
from app.domain.associations import ScenarioIncomeDomain
from tests.factory import create_fake_id
from decimal import Decimal
from datetime import datetime, timezone


class TestIncomeDomainCase:
    def test_create_scenario_income_domain(self):
        # Arrange
        scenario_id = create_fake_id()
        income_id = create_fake_id()
        max_yearly_growth_rate = Decimal("0.7")

        # Act
        scenario_income = ScenarioIncomeDomain(
            scenario_id=scenario_id,
            income_id=income_id,
            max_yearly_growth_rate=max_yearly_growth_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_income.scenario_id == scenario_id
        assert scenario_income.income_id == income_id
        assert scenario_income.max_yearly_growth_rate == max_yearly_growth_rate
