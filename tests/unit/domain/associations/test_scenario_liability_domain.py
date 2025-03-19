# from app.domain.entities import LiabilityDomain
from app.domain.association import ScenarioLiabilityDomain
from tests.unit.factories import LiabilityDomainFactory
from decimal import Decimal


class TestLiabilityDomainCase:
    def test_create_liability_domain(default_liability_domain, default_account_domain):
        # Arrange
        default_interest_rate = Decimal("0.5")
        liability = LiabilityDomainFactory(
            name="liability", interest_rate=default_interest_rate
        )
        interest_rate = Decimal("0.7")
        # Act
        scenario_liability = ScenarioLiabilityDomain(
            liability=liability,
            interest_rate=interest_rate,
        )
        # Assert
        assert scenario_liability.liability.name == "liability"
        assert scenario_liability.interest_rate != default_interest_rate
        assert scenario_liability.interest_rate == interest_rate
