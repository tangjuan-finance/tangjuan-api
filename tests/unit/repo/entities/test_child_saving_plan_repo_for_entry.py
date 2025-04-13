from app.repository.entities import ChildSavingPlanRepo
from app.infrastructure.models.entities import ChildSavingPlan
from tests.factory import (
    ChildSavingPlanDomainFactory,
    # ChildSavingAmountEntryDomainFactory,
)
import sqlalchemy as sa
from app import db


class TestChildSavingPlanRepoForEntryCase:
    def test_create_child_saving_amount_entry_through_child_saving_plan_repo(self):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan = ChildSavingPlanDomainFactory()
        child_saving_plan_from_repo = ChildSavingPlanRepo.create(child_saving_plan)

        # Act: Create new amount entries
        # NEW_AMOUNT_ENTRIES = 6
        # for _ in range(NEW_AMOUNT_ENTRIES):
        #     child_saving_amount_entry = ChildSavingAmountEntryDomainFactory(
        #         child_saving_plan_id=child_saving_plan_from_repo.id
        #     )
        #     ChildSavingPlanRepo.create_entry

        child_saving_plan_from_db = db.session.scalars(
            sa.select(ChildSavingPlan).where(
                ChildSavingPlan.id == child_saving_plan_from_repo.id
            )
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert child_saving_plan_from_repo.id == child_saving_plan_from_db.id
        assert child_saving_plan_from_repo.name == child_saving_plan_from_db.name
        assert (
            child_saving_plan_from_repo.created_at
            == child_saving_plan_from_db.created_at
        )
        assert (
            child_saving_plan_from_repo.updated_at
            == child_saving_plan_from_db.updated_at
        )

        # Assert: Ensure the child_saving_amount_entries are also saved in database
        child_saving_amount_entry_id_list_from_db = [
            entry.id for entry in child_saving_plan_from_db.child_saving_amount_entries
        ]
        for entry in child_saving_plan_from_repo.child_saving_amount_entries:
            assert entry.id in child_saving_amount_entry_id_list_from_db

    def test_update_child_saving_plan_domain_through_repo(self):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan = ChildSavingPlanDomainFactory()
        child_saving_plan_from_repo = ChildSavingPlanRepo.create(child_saving_plan)
        updated_name = "Updated ChildSavingPlan Domain"

        # Act: Update the child_saving_plan domain object (before saving)
        child_saving_plan_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_child_saving_plan = ChildSavingPlanRepo.save(
            child_saving_plan_from_repo
        )

        # Query the database to verify the updated child_saving_plan record
        child_saving_plan_from_db = db.session.scalars(
            sa.select(ChildSavingPlan).where(
                ChildSavingPlan.id == child_saving_plan_from_repo.id
            )
        ).one()

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_child_saving_plan.id == child_saving_plan_from_db.id
        assert updated_child_saving_plan.name == child_saving_plan_from_db.name
        assert (
            updated_child_saving_plan.created_at == child_saving_plan_from_db.created_at
        )
        assert (
            updated_child_saving_plan.updated_at == child_saving_plan_from_db.updated_at
        )
        # Update_at from updated_child_saving_plan should be different from the previous child_saving_plan domain (the one before update)
        assert (
            updated_child_saving_plan.updated_at
            != child_saving_plan_from_repo.updated_at
        )

    def test_get_child_saving_plan_domain_by_id_through_repo(self):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan = ChildSavingPlanDomainFactory()
        child_saving_plan_from_repo = ChildSavingPlanRepo.create(child_saving_plan)

        # Act: Update the child_saving_plan domain object (before saving)
        child_saving_plan_get_by_id = ChildSavingPlanRepo.get_by_id(
            child_saving_plan_from_repo.id
        )

        # Assert: Ensure the values match between the domain object from repo create and the domain from repo get
        assert child_saving_plan_get_by_id.id == child_saving_plan_from_repo.id
        assert child_saving_plan_get_by_id.name == child_saving_plan_from_repo.name

    def test_get_child_saving_plan_domain_list_through_repo(self, default_account):
        # Arrange: Define the params
        account_id = default_account.id
        NEW_PLANS_AMOUNT = 5

        new_child_saving_plan_list = []
        # Act: Create 5 new child_saving_plan domains
        for _ in range(NEW_PLANS_AMOUNT):
            new_child_saving_plan = ChildSavingPlanDomainFactory(owner_id=account_id)
            new_child_saving_plan_from_repo = ChildSavingPlanRepo.create(
                new_child_saving_plan
            )
            new_child_saving_plan_list.append(new_child_saving_plan_from_repo)

        # Act: Retrieve the updated child_saving_plan list
        child_saving_plans_from_repo = ChildSavingPlanRepo.get_list(
            account_id=account_id
        )

        # Assert: Check if all new created plans are in the list return from repo
        for plan in child_saving_plans_from_repo:
            assert plan in new_child_saving_plan_list

    def test_delete_child_saving_plan_domain_through_repo(self):
        # Arrange: Create an child_saving_plan domain using the factory
        child_saving_plan = ChildSavingPlanDomainFactory()
        child_saving_plan_from_repo = ChildSavingPlanRepo.create(child_saving_plan)

        # Act: Delete the child_saving_plan domain object
        ChildSavingPlanRepo.delete_by_id(child_saving_plan_from_repo.id)

        # Assert: Ensure the child_saving_plan record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(ChildSavingPlan).where(
                    ChildSavingPlan.id == child_saving_plan_from_repo.id
                )
            )
            is None
        )
