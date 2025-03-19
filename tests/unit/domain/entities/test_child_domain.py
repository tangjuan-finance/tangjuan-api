# from app.domain.entities import ChildDomain
from tests.unit.factories import ChildDomainFactory


class TestChildDomainCase:
    def test_create_child_domain(default_child_domain, default_account_domain):
        # Assert
        assert default_child_domain.name == "Default Child Domain"
        assert default_child_domain.birth_age == 34
        assert default_child_domain.independent_age == 56
        assert default_child_domain.owner_id == default_account_domain.id

    def test_factory_child_domain():
        # Arrange
        name = "Default Child Domain"
        birth_age = 34
        independent_age = 56

        # Act
        child = ChildDomainFactory(
            name=name,
            birth_age=birth_age,
            independent_age=independent_age,
        )

        # Assert
        assert child.name == name
        assert child.birth_age == birth_age
        assert child.independent_age == independent_age
