from app.domain.association import ScenarioHouseDomain
from tests.unit.factories import HouseDomainFactory
from decimal import Decimal


class TestHouseDomainCase:
    def test_create_house_domain():
        # Arrange
        default_interest_rate = Decimal("3.0")
        house = HouseDomainFactory(name="house", interest_rate=default_interest_rate)
        interest_rate = Decimal("5.0")
        # Act
        scenario_house = ScenarioHouseDomain(
            house=house,
            interest_rate=interest_rate,
        )
        # Assert
        assert scenario_house.name == "Default House Domain"
        assert scenario_house.interest_rate != default_interest_rate
        assert scenario_house.interest_rate == interest_rate
