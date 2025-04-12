from app import db
from app.infrastructure.models import ChildSavingAmountEntry
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
            child_saving_amount_entry_from_db.age
            == default_child_saving_amount_entry.age
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
        age = 15
        amount = 200000

        with pytest.raises(
            IntegrityError
        ):  # Missing child_saving_paln should raise IntegrityError
            create_entity(
                ChildSavingAmountEntry,
                age=age,
                amount=amount,
            )
