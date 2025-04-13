from app.domain.associations import ScenarioChildDomain
from tests.factory import create_fake_id
from datetime import datetime, timezone


class TestChildDomainCase:
    def test_create_scenario_child_domain(self):
        # Arrange
        scenario_id = create_fake_id()
        child_id = create_fake_id()

        default_birth_age = 34
        birth_age = 26
        # Act
        scenario_child = ScenarioChildDomain(
            scenario_id=scenario_id,
            child_id=child_id,
            birth_age=birth_age,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_child.scenario_id == scenario_id
        assert scenario_child.child_id == child_id
        assert scenario_child.birth_age != default_birth_age
        assert scenario_child.birth_age == birth_age
