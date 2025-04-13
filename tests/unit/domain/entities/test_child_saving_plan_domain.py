from app.domain.entities import ChildSavingAmountEntryDomain
from tests.factory import ChildSavingPlanDomainFactory


class TestChildSavingPlanDomainCase:
    def test_factory_child_saving_plan_domain(self):
        # Arrange: Provide params
        name = "Default Child Saving Plan Domain"
        independent_age = 22

        # Act: Create domain
        child_saving_plan = ChildSavingPlanDomainFactory(
            name=name,
            independent_age=independent_age,
        )

        # Assert: Check if the domain from factory get the same
        assert child_saving_plan.name == name
        assert child_saving_plan.independent_age == independent_age

        # Assert: The factory should has child_saving_amount_entries
        assert isinstance(child_saving_plan.child_saving_amount_entries, list)
        assert len(child_saving_plan.child_saving_amount_entries) != 0

        # Assert: Check if the obj in the child_saving_amount_entries is ChildSavingAmountEntryDomain
        for entry in child_saving_plan.child_saving_amount_entries:
            isinstance(entry, ChildSavingAmountEntryDomain)
