from app.domain.associations import ScenarioHouseDomain
from tests.unit.factories import HouseDomainFactory
from decimal import Decimal
from datetime import datetime, timezone


class TestHouseDomainCase:
    def test_create_scenario_house_domain(self, default_scenario_domain):
        # Arrange
        name = "house for scenario"

        default_interest_rate = Decimal("3.0")
        house = HouseDomainFactory(name=name, interest_rate=default_interest_rate)
        interest_rate = Decimal("5.0")
        # Act
        scenario_house = ScenarioHouseDomain(
            scenario=default_scenario_domain,
            house=house,
            interest_rate=interest_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_house.house.name == name
        assert scenario_house.interest_rate != default_interest_rate
        assert scenario_house.interest_rate == interest_rate
