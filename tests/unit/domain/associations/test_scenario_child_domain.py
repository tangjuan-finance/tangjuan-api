from app.domain.association import ScenarioChildDomain
from tests.unit.factories import ChildDomainFactory


class TestChildDomainCase:
    def test_create_child_domain(default_child_domain, default_account_domain):
        # Arrange
        default_birth_age = 34
        child = ChildDomainFactory(name="child", birth_age=default_birth_age)
        birth_age = 26
        # Act
        scenario_child = ScenarioChildDomain(
            child=child,
            birth_age=birth_age,
        )
        # Assert
        assert scenario_child.child.name == "child"
        assert scenario_child.birth_age != default_birth_age
        assert scenario_child.birth_age == birth_age
