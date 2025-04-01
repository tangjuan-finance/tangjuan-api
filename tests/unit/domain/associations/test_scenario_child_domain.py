from app.domain.associations import ScenarioChildDomain
from tests.unit.factories import ChildDomainFactory
from datetime import datetime, timezone


class TestChildDomainCase:
    def test_create_scenario_child_domain(self, default_scenario_domain):
        # Arrange
        name = "child for scenario"

        default_birth_age = 34
        child = ChildDomainFactory(name=name, birth_age=default_birth_age)
        birth_age = 26
        # Act
        scenario_child = ScenarioChildDomain(
            scenario_id=default_scenario_domain.id,
            child_id=child.id,
            birth_age=birth_age,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_child.scenario_id == default_scenario_domain.id
        assert scenario_child.child_id == child.id
        assert scenario_child.birth_age != default_birth_age
        assert scenario_child.birth_age == birth_age
