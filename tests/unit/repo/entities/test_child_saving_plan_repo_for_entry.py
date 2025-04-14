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
    def test_create_child_saving_amount_entry_through_child_saving_plan_repo(self):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan_from_repo = self._create_new_child_saving_plan_by_repo()

        # Act: Create and save new amount entries to database
        NEW_AMOUNT_ENTRIES = 6
        entry_list = self._create_amount_entries_by_repo(
            child_saving_plan_id=child_saving_plan_from_repo.id,
            length=NEW_AMOUNT_ENTRIES,
        )

        # Assert: Get the plan from database, the new added amount entries should be there
        plan_from_repo = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id=child_saving_plan_from_repo.id
        )

        for entry in entry_list:
            assert entry in plan_from_repo.child_saving_amount_entries

    def test_update_child_saving_plan_domain_through_repo(self):
        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries()
        plan_id = child_saving_plan_from_repo.id

        # Arrange: Get one entry
        target_entry = child_saving_plan_from_repo.child_saving_amount_entries[0]
        entry_id = target_entry.id

        # Act: Update the child_saving_amount_entry domain object (before saving)
        update_end_age = target_entry.end_age + 2
        update_amount = target_entry.amount + 15000

        target_entry.end_age = update_end_age
        target_entry.amount = update_amount

        ChildSavingPlanRepo.update_entry(entry=target_entry)

        # Assert: Plan get from database should reflect this update
        updated_child_saving_plan = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_id=plan_id
        )

        entry_in_planfrom_repo = [
            entry
            for entry in updated_child_saving_plan.child_saving_amount_entries
            if entry.id == entry_id
        ][0]

        # Assert: Check the id is the same
        assert entry_in_planfrom_repo.id == entry_id

        # Assert: Check the non-updated field should be the same
        assert entry_in_planfrom_repo.start_age == target_entry.start_age

        # Assert: Check the non-updated field as updated
        assert entry_in_planfrom_repo.end_age == update_end_age
        assert entry_in_planfrom_repo.amount == update_amount

    def test_get_child_saving_plan_domain_by_id_through_repo(self):
        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries()

        # Arrange: Get entry id
        entry = child_saving_plan_from_repo.child_saving_amount_entries[0]
        entry_id = entry.id

        # Act: Get entry by repo service
        entry_from_repo = ChildSavingPlanRepo.get_entry_by_id(entry_id=entry_id)

        # Assert: Both entry should be the same
        assert entry.id == entry_from_repo.id
        assert entry.amount == entry_from_repo.amount
        assert entry == entry_from_repo

    def test_get_child_saving_plan_domain_list_through_repo(self):
        # Arrange: Define the params
        NEW_AMOUNT_ENTRIES = 6

        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries(
            length=NEW_AMOUNT_ENTRIES
        )
        entry_list = child_saving_plan_from_repo.child_saving_amount_entries

        # Act: Get entries by repo
        entry_list_from_repo = ChildSavingPlanRepo.list_entries(
            child_saving_plan_id=child_saving_plan_from_repo.id
        )

        # Assert: Entry list from repo should be the same as the created one
        assert len(entry_list) == NEW_AMOUNT_ENTRIES
        assert len(entry_list_from_repo) == len(entry_list)

        for entry in entry_list:
            assert entry in entry_list_from_repo

    def test_delete_child_saving_plan_domain_through_repo(self):
        # Arrange: Create a plan with multiple entries
        child_saving_plan_from_repo = self._create_plan_with_amount_entries()
        plan_id = child_saving_plan_from_repo.id

        # Arrange: Get one entry
        target_entry = child_saving_plan_from_repo.child_saving_amount_entries[0]
        entry_id = target_entry.id

        # Act: Delete the entry
        ChildSavingPlanRepo.delete_entry_by_id(entry_id=entry_id)

        # Assert: The deleted entry should not in plan
        plan_form_repo = ChildSavingPlanRepo.get_by_id(child_saving_plan_id=plan_id)
        entry_id_list_from_repo = [
            entry.id for entry in plan_form_repo.child_saving_amount_entries
        ]
        assert entry_id not in entry_id_list_from_repo

        # Assert: THe deleted entry is not in database as well
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
        plan_id = plan.id

        # Create amount entries
        self._create_amount_entries_by_repo(child_saving_plan_id=plan_id, length=length)

        # Get updated plan
        return ChildSavingPlanRepo.get_by_id(child_saving_plan_id=plan_id)

    def _create_new_child_saving_plan_by_repo(
        self, owner_id: Optional[str] = None
    ) -> ChildSavingPlanDomain:
        given_id = owner_id if owner_id else create_fake_id()
        child_saving_plan = ChildSavingPlanDomainFactory(owner_id=given_id)

        return ChildSavingPlanRepo.create(child_saving_plan)

    def _create_amount_entries_by_repo(
        self, child_saving_plan_id: str, length: int = 3
    ) -> list[ChildSavingAmountEntryDomain]:
        entry_list = []
        for idx in range(length):
            new_entry = self._create_amount_entry_by_repo(
                child_saving_plan_id=child_saving_plan_id
            )
            entry_list.append(new_entry)

        return entry_list

    def _create_amount_entry_by_repo(
        self,
        child_saving_plan_id: str,
    ) -> ChildSavingAmountEntryDomain:
        entry = ChildSavingAmountEntryDomainFactory(
            child_saving_plan_id=child_saving_plan_id,
        )
        return ChildSavingPlanRepo.add_entry(entry)
