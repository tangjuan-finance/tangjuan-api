from app import db
from app.infrastructure.models import ChildSavingPlan, Child, ChildSavingAmountEntry
import sqlalchemy as sa
from ..factories import create_entity


class TestChildSavingPlanModelCase:
    def test_default_child_saving_plan(self, default_child_saving_plan):
        # Act
        child_saving_plan_from_db = db.session.scalar(
            sa.select(ChildSavingPlan).where(
                ChildSavingPlan.id == default_child_saving_plan.id
            )
        )

        # Assert
        assert child_saving_plan_from_db.name == default_child_saving_plan.name
        assert (
            child_saving_plan_from_db.independent_age
            == default_child_saving_plan.independent_age
        )
        assert child_saving_plan_from_db.owner_id == default_child_saving_plan.owner_id
        assert (
            child_saving_plan_from_db.created_at == default_child_saving_plan.created_at
        )
        assert (
            child_saving_plan_from_db.updated_at == default_child_saving_plan.updated_at
        )

    def test_default_child_saving_plan_with_child(
        self, default_child, default_account_domain
    ):
        # Arrange: Given param
        name = "Another Child Saving Plan"
        independent_age = 22

        # Arrange: Create child_saving_plan
        child_saving_plan = create_entity(
            ChildSavingPlan,
            name=name,
            independent_age=independent_age,
            owner_id=default_account_domain.id,
        )

        # Arrange: Add the default child to the plan
        child_saving_plan.children.append(default_child)
        db.session.commit()

        # Act: Get child_saving_plan from database
        child_saving_plan_from_db = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan.id)
        )

        # Assert: If the plan retrieve from the database contain default_child
        assert child_saving_plan_from_db.children[0] == default_child

    def test_default_child_saving_plan_with_amount_entry(
        self, default_child_saving_amount_entry, default_account_domain
    ):
        # Arrange: Given param
        name = "Child Saving Plan with amount entry"
        independent_age = 22

        # Arrange: Create child_saving_plan
        child_saving_plan = create_entity(
            ChildSavingPlan,
            name=name,
            independent_age=independent_age,
            owner_id=default_account_domain.id,
        )

        # Arrange: Add the default child to the plan
        child_saving_plan.child_saving_amount_entries.append(
            default_child_saving_amount_entry
        )
        db.session.commit()

        # Act: Get child_saving_plan from database
        child_saving_plan_from_db = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan.id)
        )

        # Assert: If the plan retrieve from the database contain default_child
        assert (
            child_saving_plan_from_db.child_saving_amount_entries[0]
            == default_child_saving_amount_entry
        )

    def test_default_child_saving_plan_with_children(self, default_account_domain):
        # Arrange: Given param
        name = "Child Saving Plan with a few of children"
        independent_age = 22

        # Arrange: Create child_saving_plan
        child_saving_plan = create_entity(
            ChildSavingPlan,
            name=name,
            independent_age=independent_age,
            owner_id=default_account_domain.id,
        )

        # Arrange: Create a few of children entities and add it to child_saving_plan
        NEW_CHILDREN_AMOUNT = 5
        child_list = []
        for count in range(NEW_CHILDREN_AMOUNT):
            name = f"Child No. {count}"
            birth_age = 34 + count * 2
            new_child = create_entity(
                Child,
                name=name,
                birth_age=birth_age,
                parent=default_account_domain,
                child_saving_plan=child_saving_plan,
            )
            child_list.append(new_child)

        # Act: Get child_saving_plan from database
        child_saving_plan_from_db = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan.id)
        )

        # Assert: If the plan retrieve from the database contain default_child
        assert len(child_saving_plan_from_db.children) == NEW_CHILDREN_AMOUNT
        for child in child_list:
            assert child in child_saving_plan_from_db.children

    def test_default_child_saving_plan_with_amount_entries(
        self, default_account_domain
    ):
        # Arrange: Given param
        name = "Child Saving Plan with a few of amount entries"
        independent_age = 22

        # Arrange: Create child_saving_plan
        child_saving_plan = create_entity(
            ChildSavingPlan,
            name=name,
            independent_age=independent_age,
            owner_id=default_account_domain.id,
        )

        # Arrange: Create a few of children entities and add it to child_saving_plan
        NEW_AMOUNT_ENTRIES = 10
        entry_list = []
        for count in range(NEW_AMOUNT_ENTRIES):
            name = f"Entry No. {count}"
            start_age = count * 2
            end_age = start_age + 1
            amount = 100000 + count * 10000
            new_amount_entry = create_entity(
                ChildSavingAmountEntry,
                name=name,
                start_age=start_age,
                end_age=end_age,
                amount=amount,
                child_saving_plan=child_saving_plan,
            )
            entry_list.append(new_amount_entry)

        # Act: Get child_saving_plan from database
        child_saving_plan_from_db = db.session.scalar(
            sa.select(ChildSavingPlan).where(ChildSavingPlan.id == child_saving_plan.id)
        )

        # Assert: If the plan retrieve from the database contain default_child
        assert (
            len(child_saving_plan_from_db.child_saving_amount_entries)
            == NEW_AMOUNT_ENTRIES
        )
        for entry in entry_list:
            assert entry in child_saving_plan_from_db.child_saving_amount_entries
