import pytest
from tests.factory import (
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    create_fake_id,
)
from app.domain.entities import (
    ChildSavingPlanDomain,
    ChildSavingAmountEntryDomain,
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

    def _add_new_entry(
        self, plan: ChildSavingPlanDomain, payload: ChildSavingAmountEntryDomain
    ) -> ChildSavingAmountEntryDomain:
        return plan.add_entry(
            name=payload.name,
            start_age=payload.start_age,
            end_age=payload.end_age,
            amount=payload.amount,
            description=payload.description,
        )

    def test_add_entry(self, default_child_saving_plan_domain):
        # Arrange: Create entry attrs
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

    def test_get_entry_by_id(self, default_child_saving_plan_domain):
        # Arrange: Create a new entry
        new_entry_payload = ChildSavingAmountEntryDomainFactory()
        entry = self._add_new_entry(
            plan=default_child_saving_plan_domain, payload=new_entry_payload
        )

        # Act: Get entry by id
        entry_from_plan = default_child_saving_plan_domain.get_entry_by_id(
            entry_id=entry.id
        )

        # Assert: Check if the entry could be retrieved
        assert entry_from_plan is not None

        # Assert: Check if the entry from plan has the same attr as given
        assert entry_from_plan.name == new_entry_payload.name
        assert entry_from_plan.start_age == new_entry_payload.start_age
        assert entry_from_plan.end_age == new_entry_payload.end_age
        assert entry_from_plan.amount == new_entry_payload.amount
        assert entry_from_plan.description == new_entry_payload.description

    def test_get_entries(self, default_child_saving_plan_domain):
        # Arrange: Create a few of new entries
        NEW_ENTRIES = 10
        new_entry_list = [
            self._add_new_entry(
                plan=default_child_saving_plan_domain,
                payload=ChildSavingAmountEntryDomainFactory(),
            )
            for _ in range(NEW_ENTRIES)
        ]

        # Act: Get entries by id
        entry_list_from_plan = default_child_saving_plan_domain.list_entries()

        # Assert: Check if the created entries are all in the entry list
        assert all(entry in entry_list_from_plan for entry in new_entry_list)

    def test_update_entry(self, default_child_saving_plan_domain):
        # Arrange: Create an entry to the default plan
        payload = ChildSavingAmountEntryDomainFactory()
        entry = self._add_new_entry(
            plan=default_child_saving_plan_domain, payload=payload
        )

        # Act: Update the entry
        update_amount = entry.amount + 100000
        default_child_saving_plan_domain.update_entry_by_id(
            entry_id=entry.id, amount=update_amount
        )

        # Arrange: Get the update entry from the plan
        entry_from_plan = default_child_saving_plan_domain.get_entry_by_id(
            entry_id=entry.id
        )

        # Assert: Check if the target entry update its value
        assert entry_from_plan.amount == update_amount

    def test_delete_entry(self, default_child_saving_plan_domain):
        # Arrange: Create an entry to the default plan
        payload = ChildSavingAmountEntryDomainFactory()
        entry = self._add_new_entry(
            plan=default_child_saving_plan_domain, payload=payload
        )

        # Act: Delete the entry
        default_child_saving_plan_domain.remove_entry_by_id(entry_id=entry.id)

        # Assert: Ensure the entry is not in the plan
        assert entry not in default_child_saving_plan_domain.child_saving_amount_entries

    def test_add_entry_with_incomplete_attr(self, default_child_saving_plan_domain):
        # Arrange: Create entry attrs
        new_entry_payload = ChildSavingAmountEntryDomainFactory()

        # Assert: Add an entry which missing required positional argument to the plan should raise TypeError
        with pytest.raises(TypeError):
            default_child_saving_plan_domain.add_entry(
                name=new_entry_payload.name,
                start_age=new_entry_payload.start_age,
                end_age=new_entry_payload.end_age,
                description=new_entry_payload.description,
            )

    def test_update_entry_with_invalid_attr(self, default_child_saving_plan_domain):
        # Arrange: Create an entry to the default plan
        payload = ChildSavingAmountEntryDomainFactory()
        entry = self._add_new_entry(
            plan=default_child_saving_plan_domain, payload=payload
        )

        # Act: Update the entry
        update_amount = entry.amount + 100000
        invalid_attr = {"invalid": "this_is_a_invalid_attr"}
        with pytest.raises(ValueError):
            default_child_saving_plan_domain.update_entry_by_id(
                entry_id=entry.id, amount=update_amount, **invalid_attr
            )

    def test_get_entry_by_invalid_id(self, default_child_saving_plan_domain):
        # Arrange: Create a fake id
        fake_id = create_fake_id()

        # Assert: Get entry by invalid id should return None
        not_existed_entry = default_child_saving_plan_domain.get_entry_by_id(
            entry_id=fake_id
        )

        assert not_existed_entry is None

    def test_list_empty_entry(self, default_child_saving_plan_domain):
        # Assert: Get the entry list from default plan should return empty list
        assert default_child_saving_plan_domain.list_entries() == []

    def test_delete_not_existed_entry(self, default_child_saving_plan_domain):
        # Arrange: Create a fake id
        fake_id = create_fake_id()

        # Assert: Delete not existed entry should raise ValueError
        with pytest.raises(ValueError):
            default_child_saving_plan_domain.remove_entry_by_id(entry_id=fake_id)
