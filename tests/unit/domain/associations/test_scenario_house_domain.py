from app.domain.associations import ScenarioHouseDomain
from tests.factory import create_fake_id
from decimal import Decimal
from datetime import datetime, timezone


class TestHouseDomainCase:
    def test_create_scenario_house_domain(self):
        # Arrange
        scenario_id = create_fake_id()
        house_id = create_fake_id()
        interest_rate = Decimal("5.0")
        # Act
        scenario_house = ScenarioHouseDomain(
            scenario_id=scenario_id,
            house_id=house_id,
            interest_rate=interest_rate,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_house.scenario_id == scenario_id
        assert scenario_house.house_id == house_id
        assert scenario_house.interest_rate == interest_rate
