import pytest
from app.domain.entities import ChildDomain
from tests.factory import (
    AccountDomainFactory,
    ChildDomainFactory,
    ChildSavingPlanDomainFactory,
)


class TestChildDomainCase:
    def test_factory_child_domain(self):
        # Arrange
        name = "Default Child Domain"
        birth_age = 34
        independent_age = 56
        child_saving_plan_id = ChildSavingPlanDomainFactory().id

        # Act
        child = ChildDomainFactory(
            name=name,
            birth_age=birth_age,
            independent_age=independent_age,
            child_saving_plan_id=child_saving_plan_id,
        )

        # Assert
        assert child.name == name
        assert child.birth_age == birth_age
        assert child.independent_age == independent_age
        assert child.child_saving_plan_id == child_saving_plan_id

    def test_factory_child_domain_without_parent(self):
        # Arrange: Provide params
        name = "Default Child Domain"
        birth_age = 34
        independent_age = 56
        child_saving_plan_id = ChildSavingPlanDomainFactory().id

        # Assert: Create Child Obj without parent should raise TypeError
        with pytest.raises(TypeError):
            ChildDomain(
                name=name,
                birth_age=birth_age,
                independent_age=independent_age,
                child_saving_plan_id=child_saving_plan_id,
            )

    def test_factory_child_domain_without_plan(self):
        # Arrange: Provide params
        name = "Default Child Domain"
        birth_age = 34
        independent_age = 56
        parent = AccountDomainFactory()

        # Assert: Create Child Obj without plan should raise TypeError
        with pytest.raises(TypeError):
            ChildDomain(
                name=name,
                birth_age=birth_age,
                independent_age=independent_age,
                parent=parent,
            )
