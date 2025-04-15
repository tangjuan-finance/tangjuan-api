import pytest
from app.domain.entities import ChildDomain
from tests.factory import AccountDomainFactory, ChildDomainFactory, create_fake_id


class TestChildDomainCase:
    def test_create_child_domain(self, default_account_domain):
        # Arrange
        name = "Default Child Domain"
        birth_age = 34
        child_saving_plan_id = create_fake_id()

        # Act
        child = ChildDomain(
            name=name,
            birth_age=birth_age,
            child_saving_plan_id=child_saving_plan_id,
            parent=default_account_domain,
        )

        # Assert
        assert isinstance(child.id, str)
        assert len(child.id) == 13
        assert child.name == name
        assert child.birth_age == birth_age
        assert child.child_saving_plan_id == child_saving_plan_id
        assert child.parent == default_account_domain

    def test_factory_child_domain(self):
        # Arrange
        name = "Default Child Domain"
        birth_age = 34
        child_saving_plan_id = create_fake_id()

        # Act
        child = ChildDomainFactory(
            name=name,
            birth_age=birth_age,
            child_saving_plan_id=child_saving_plan_id,
        )

        # Assert
        assert isinstance(child.id, str)
        assert len(child.id) == 13
        assert child.name == name
        assert child.birth_age == birth_age
        assert child.child_saving_plan_id == child_saving_plan_id

    def test_factory_child_domain_without_parent(self):
        # Arrange: Provide params
        name = "Default Child Domain"
        birth_age = 34
        child_saving_plan_id = create_fake_id()

        # Assert: Create Child Obj without parent should raise TypeError
        with pytest.raises(TypeError):
            ChildDomain(
                name=name,
                birth_age=birth_age,
                child_saving_plan_id=child_saving_plan_id,
            )

    def test_factory_child_domain_without_plan(self):
        # Arrange: Provide params
        name = "Default Child Domain"
        birth_age = 34
        parent = AccountDomainFactory()

        # Assert: Create Child Obj without plan should raise TypeError
        with pytest.raises(TypeError):
            ChildDomain(
                name=name,
                birth_age=birth_age,
                parent=parent,
            )
