import pytest
from app import db
from app.infrastructure.models import Child, ChildSavingPlan
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from ..factories import create_entity


class TestChildModelCase:
    def test_default_child(self, default_child):
        # Act
        child_from_db = db.session.scalar(
            sa.select(Child).where(Child.id == default_child.id)
        )

        # Assert
        assert child_from_db.name == default_child.name
        assert child_from_db.birth_age == default_child.birth_age
        assert child_from_db.independent_age == default_child.independent_age
        assert child_from_db.created_at == default_child.created_at
        assert child_from_db.updated_at == default_child.updated_at
        assert child_from_db.parent_id == default_child.parent_id
        assert child_from_db.child_saving_plan_id == default_child.child_saving_plan_id

    def test_default_child_not_set_saving_plan(self, default_account_domain):
        name = "Default Child"
        birth_age = 34
        independent_age = 56

        with pytest.raises(
            IntegrityError
        ):  # Missing child_saving_paln should raise IntegrityError
            create_entity(
                Child,
                parent=default_account_domain,
                name=name,
                birth_age=birth_age,
                independent_age=independent_age,
            )

    def test_default_child_change_saving_plan(self, default_child):
        # Arrange: Store the origin plan
        origin_plan = default_child.child_saving_plan

        # Arrange: Create new child_saving_plan
        name = "Updated Child Saving Plan"

        new_plan = create_entity(
            ChildSavingPlan,
            name=name,
        )

        # Act: Update the new plan
        default_child.child_saving_plan = new_plan
        db.session.commit()

        # Assert: The child get from the db should own the new plan
        child_from_db = db.session.scalar(
            sa.select(Child).where(Child.id == default_child.id)
        )

        assert child_from_db.child_saving_plan == new_plan
        assert child_from_db.child_saving_plan != origin_plan
