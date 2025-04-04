# from app.domain.entities import ChildDomain
from tests.factory import ChildDomainFactory


class TestChildDomainCase:
    def test_factory_child_domain(self):
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
