from app import db
from app.infrastructure.models import ChildSavingAmountEntry, ChildSavingPlan
import sqlalchemy as sa
import pytest
from sqlalchemy.exc import IntegrityError
from ..factories import create_entity


class TestChildSavingAmountEntryModelCase:
    def test_default_child_saving_amount_entry(self, default_child_saving_amount_entry):
        # Act
        child_saving_amount_entry_from_db = db.session.scalar(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.id == default_child_saving_amount_entry.id
            )
        )

        # Assert
        assert (
            child_saving_amount_entry_from_db.start_age
            == default_child_saving_amount_entry.start_age
        )
        assert (
            child_saving_amount_entry_from_db.end_age
            == default_child_saving_amount_entry.end_age
        )
        assert (
            child_saving_amount_entry_from_db.amount
            == default_child_saving_amount_entry.amount
        )
        assert (
            child_saving_amount_entry_from_db.created_at
            == default_child_saving_amount_entry.created_at
        )
        assert (
            child_saving_amount_entry_from_db.updated_at
            == default_child_saving_amount_entry.updated_at
        )
        assert (
            child_saving_amount_entry_from_db.child_saving_plan_id
            == default_child_saving_amount_entry.child_saving_plan_id
        )

    def test_default_child_saving_amount_entry_without_saving_plan(self):
        start_age = 12
        end_age = 15
        amount = 200000

        with pytest.raises(
            IntegrityError
        ):  # Missing child_saving_paln should raise IntegrityError
            create_entity(
                ChildSavingAmountEntry,
                start_age=start_age,
                end_age=end_age,
                amount=amount,
            )

    def test_default_child_change_saving_plan(
        self, default_child_saving_amount_entry, default_account_domain
    ):
        # Arrange: Store the origin plan
        origin_plan = default_child_saving_amount_entry.child_saving_plan

        # Arrange: Create new child_saving_plan
        name = "Updated Child Saving Plan"

        new_plan = create_entity(
            ChildSavingPlan,
            name=name,
            owner_id=default_account_domain.id,
        )

        # Act: Update the new plan
        default_child_saving_amount_entry.child_saving_plan = new_plan
        db.session.commit()

        # Assert: The child get from the db should own the new plan
        child_saving_amount_entry_from_db = db.session.scalar(
            sa.select(ChildSavingAmountEntry).where(
                ChildSavingAmountEntry.id == default_child_saving_amount_entry.id
            )
        )

        assert child_saving_amount_entry_from_db.child_saving_plan == new_plan
        assert child_saving_amount_entry_from_db.child_saving_plan != origin_plan
