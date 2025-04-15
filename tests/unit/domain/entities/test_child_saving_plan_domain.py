from tests.factory import (
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    # create_fake_id,
)
from app.domain.entities import (
    ChildSavingPlanDomain,
    # ChildSavingAmountEntryDomain,
    # EntityDomain,
)


class TestChildSavingPlanDomainCase:
    def test_create_child_saving_plan_domain(self, default_account_domain):
        # Arrange: Provide params
        name = "Default Child Saving Plan Domain"
        independent_age = 22

        # Act: Create domain
        child_saving_plan = ChildSavingPlanDomain(
            name=name,
            independent_age=independent_age,
            owner_id=default_account_domain.id,
        )

        # Assert: Check if the domain from factory get the same
        assert isinstance(child_saving_plan.id, str)
        assert len(child_saving_plan.id) == 13
        assert child_saving_plan.name == name
        assert child_saving_plan.independent_age == independent_age
        assert child_saving_plan.owner_id == default_account_domain.id

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
        assert isinstance(child_saving_plan.id, str)
        assert len(child_saving_plan.id) == 13
        assert child_saving_plan.name == name
        assert child_saving_plan.independent_age == independent_age

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

    def test_add_entry(self, default_child_saving_plan_domain):
        # Arrange: create entry attrs
        new_entry_payload = ChildSavingAmountEntryDomainFactory()

        # Act: Add an entry to the plan with the given attrs
        return_entry = default_child_saving_plan_domain.add_entry(
            name=new_entry_payload.name,
            start_age=new_entry_payload.start_age,
            end_age=new_entry_payload.end_age,
            amount=new_entry_payload.amount,
            description=new_entry_payload.description,
        )

        # Assert: Check if the entry is add to the plan
        entry_from_plan = [
            entry
            for entry in default_child_saving_plan_domain.child_saving_amount_entries
            if entry.id == return_entry.id
        ][0]
        assert entry_from_plan is not None

        # Assert: Check if the entry from plan has the same attr as given
        assert entry_from_plan.name == new_entry_payload.name
        assert entry_from_plan.start_age == new_entry_payload.start_age
        assert entry_from_plan.end_age == new_entry_payload.end_age
        assert entry_from_plan.amount == new_entry_payload.amount
        assert entry_from_plan.description == new_entry_payload.description

    def _add_new_entry(self, plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
        new_entry_payload = ChildSavingAmountEntryDomainFactory()
        plan.add_entry(
            name=new_entry_payload.name,
            start_age=new_entry_payload.start_age,
            end_age=new_entry_payload.end_age,
            amount=new_entry_payload.amount,
            description=new_entry_payload.description,
        )
        return plan
