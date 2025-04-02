# from app.domain.entities import LiabilityDomain
from app.domain.associations import ScenarioLiabilityDomain
from tests.factory import LiabilityDomainFactory
from decimal import Decimal
from datetime import datetime, timezone


class TestLiabilityDomainCase:
    def test_create_scenario_liability_domain(self, default_scenario_domain):
        # Arrange
        name = "liability for scenario"

        default_interest_rate = Decimal("0.5")
        liability = LiabilityDomainFactory(
            name=name, interest_rate=default_interest_rate
        )
        interest_rate = Decimal("0.7")
        allocation_percentage = Decimal("0.35")
        # Act
        scenario_liability = ScenarioLiabilityDomain(
            scenario_id=default_scenario_domain.id,
            liability_id=liability.id,
            allocation_percentage=allocation_percentage,
            interest_rate=interest_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_liability.scenario_id == default_scenario_domain.id
        assert scenario_liability.liability_id == liability.id
        assert scenario_liability.interest_rate != default_interest_rate
        assert scenario_liability.interest_rate == interest_rate
        assert scenario_liability.allocation_percentage == allocation_percentage
