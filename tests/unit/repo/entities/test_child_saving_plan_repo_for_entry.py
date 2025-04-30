from app.repository.entities import ChildSavingPlanRepo
from app.domain.entities import ChildSavingPlanDomain, ChildSavingAmountEntryDomain
from app.infrastructure.models.entities import ChildSavingAmountEntry
from tests.factory import (
    ChildSavingPlanDomainFactory,
    ChildSavingAmountEntryDomainFactory,
    create_fake_id,
)
from typing import Optional
import sqlalchemy as sa
from app import db


class TestChildSavingPlanRepoForEntryCase:
    def test_create_child_saving_amount_entry_through_child_saving_plan_repo(
        self, default_account
    ):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan_from_repo = self._create_new_child_saving_plan_by_repo(
            owner_id=default_account.id
        )

        # Act: Create and save new amount entries to database
        NEW_AMOUNT_ENTRIES = 6
        entry_list = []
        for idx in range(NEW_AMOUNT_ENTRIES):
            # Create the payload from the factory
            payload = ChildSavingAmountEntryDomainFactory()

            # Save tne entry to the plan by domain service
            new_entry = child_saving_plan_from_repo.add_entry(
                name=payload.name,
                start_age=payload.start_age,
                end_age=payload.end_age,
                amount=payload.amount,
                description=payload.description,
            )

            entry_list.append(new_entry)

        # Act: Save the update to database by repo
        ChildSavingPlanRepo.save(child_saving_plan_from_repo)

        # Assert: Get the plan from database, the new added amount entries should be there
        plan_from_repo = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id=child_saving_plan_from_repo.id
        )
        entry_id_list_from_repo = [
            entry.id for entry in plan_from_repo.child_saving_amount_entries
        ]

        for entry in entry_list:
            assert entry.id in entry_id_list_from_repo

    def test_update_child_saving_plan_domain_through_repo(self, default_account):
        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries(
            owner_id=default_account.id
        )

        # Arrange: Get one entry
        target_entry = child_saving_plan_from_repo.child_saving_amount_entries[0]
        entry_id = target_entry.id

        # Arrange: Create the update attrs for the targeted entry
        update_end_age = target_entry.end_age + 2
        update_amount = target_entry.amount + 15000
        update_attrs = {
            "end_age": update_end_age,
            "amount": update_amount,
        }

        # Act: Update the entry by the plan domain with the update attrs
        child_saving_plan_from_repo.update_entry_by_id(
            entry_id=entry_id, **update_attrs
        )

        # Act: Save the change
        ChildSavingPlanRepo.save(child_saving_plan=child_saving_plan_from_repo)

        # Assert: Plan get from database should reflect this update
        updated_child_saving_plan = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id=child_saving_plan_from_repo.id
        )

        entry_from_repo = updated_child_saving_plan.get_entry_by_id(entry_id=entry_id)

        # Assert: Check the non-updated field should be the same
        assert entry_from_repo.start_age == target_entry.start_age

        # Assert: Check the updated field as updated
        assert entry_from_repo.end_age == update_end_age
        assert entry_from_repo.amount == update_amount

    def test_delete_child_saving_plan_domain_through_repo(self, default_account):
        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries(
            owner_id=default_account.id
        )

        # Arrange: Get one entry
        target_entry = child_saving_plan_from_repo.child_saving_amount_entries[0]
        entry_id = target_entry.id

        # Act: Remove the entry by the plan domain with the update attrs
        child_saving_plan_from_repo.remove_entry_by_id(entry_id=entry_id)

        # Act: Save the change
        ChildSavingPlanRepo.save(child_saving_plan=child_saving_plan_from_repo)

        # Assert: Plan get from database should reflect this update
        updated_child_saving_plan = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id=child_saving_plan_from_repo.id
        )
        # Assert: Get removed id from the plan should return None
        entry_from_repo = updated_child_saving_plan.get_entry_by_id(entry_id=entry_id)

        # Assert: Check the non-updated field should be the same
        assert entry_from_repo is None

        # Assert: The deleted entry is not in database as well
        assert (
            db.session.scalar(
                sa.select(ChildSavingAmountEntry).where(
                    ChildSavingAmountEntry.id == entry_id
                )
            )
            is None
        )

    def _create_plan_with_amount_entries(
        self, owner_id: Optional[str] = None, length: Optional[int] = None
    ) -> ChildSavingPlanDomain:
        # Create plan
        plan = self._create_new_child_saving_plan_by_repo(owner_id=owner_id)

        # Create amount entries and return the update plan
        if length is None:
            return self._add_amount_entries_by_repo(child_saving_plan=plan)
        else:
            return self._add_amount_entries_by_repo(
                child_saving_plan=plan, length=length
            )

    def _create_new_child_saving_plan_by_repo(
        self, owner_id: Optional[str] = None
    ) -> ChildSavingPlanDomain:
        given_id = owner_id if owner_id else create_fake_id()
        child_saving_plan = ChildSavingPlanDomainFactory(owner_id=given_id)

        return ChildSavingPlanRepo.create(child_saving_plan)

    def _add_amount_entries_by_repo(
        self, child_saving_plan: ChildSavingPlanDomain, length: int = 3
    ) -> list[ChildSavingAmountEntryDomain]:
        for idx in range(length):
            # Create the payload from the factory
            payload = ChildSavingAmountEntryDomainFactory()

            # Save tne entry to the plan by domain service
            child_saving_plan.add_entry(
                name=payload.name,
                start_age=payload.start_age,
                end_age=payload.end_age,
                amount=payload.amount,
                description=payload.description,
            )

        # Save the update to database by repo, and return the update plan
        return ChildSavingPlanRepo.save(child_saving_plan)
