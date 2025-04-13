# from app.domain.entities import ChildSavingAmountEntryDomain
from tests.factory import (
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    create_fake_id,
)


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

        # Arrange: Given fake id to the child saving plan
        child_saving_plan.id = create_fake_id()

        # Arrange: Create a few of fake saving amount entries and add to the plan
        NEW_ENTRIES = 5
        new_entry_list = []
        for idx in range(NEW_ENTRIES):
            new_entry = ChildSavingAmountEntryDomainFactory(
                child_saving_plan_id=child_saving_plan.id
            )
            child_saving_plan.child_saving_amount_entries.append(new_entry)
            new_entry_list.append(new_entry)

        # Assert: The factory should has child_saving_amount_entries
        assert isinstance(child_saving_plan.child_saving_amount_entries, list)
        assert len(child_saving_plan.child_saving_amount_entries) == NEW_ENTRIES

        # Assert: Check if the obj in the child_saving_amount_entries is ChildSavingAmountEntryDomain
        for entry in child_saving_plan.child_saving_amount_entries:
            assert entry in new_entry_list
