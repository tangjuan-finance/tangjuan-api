from tests.factory import (
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    # create_fake_id,
)
from app.domain.entities import ChildSavingPlanDomain
# ,
#     # ChildSavingAmountEntryDomain,
#     EntityDomain,
# )
# from datetime import datetime, timezone


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

    # def test_add_entry(self, default_child_saving_plan_domain):
    #     # Arrange: Fake save the plan to get the plan id
    #     plan = self._fake_save_plan(default_child_saving_plan_domain)

    #     # Arrange: create entry attrs
    #     new_entry_payload = ChildSavingAmountEntryDomainFactory()

    #     # Act: Add an entry to the plan with the given attrs
    #     plan.add_entry(
    #         name=new_entry_payload.name,
    #         start_age=new_entry_payload.start_age,
    #         end_age=new_entry_payload.end_age,
    #         amount=new_entry_payload.amount,
    #         description=new_entry_payload.description,
    #     )

    #     # Assert: Check if the

    # def _add_new_entry(self, plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
    #     new_entry_payload = ChildSavingAmountEntryDomainFactory()
    #     plan.add_entry(
    #         name=new_entry_payload.name,
    #         start_age=new_entry_payload.start_age,
    #         end_age=new_entry_payload.end_age,
    #         amount=new_entry_payload.amount,
    #         description=new_entry_payload.description,
    #     )
    #     return plan

    # def _fake_save_plan(self, plan: ChildSavingPlanDomain) -> ChildSavingPlanDomain:
    #     # fake save plan
    #     fake_saved_plan = self._fake_save(plan)

    #     fake_saved_entry_list = []
    #     for entry in plan.child_saving_amount_entries:
    #         fake_saved_entry = self._fake_save(entry)
    #         fake_saved_entry_list.append(fake_saved_entry)

    #     fake_saved_plan.child_saving_amount_entries = fake_saved_entry_list
    #     return fake_saved_plan

    # def _fake_save(self, entity: EntityDomain) -> EntityDomain:
    #     entity.id = create_fake_id()

    #     if not entity.created_at:
    #         entity.created_at = datetime.now(timezone.utc)

    #     entity.updated_at = datetime.now(timezone.utc)

    #     return entity
