from app import db
from app.models import Child
import sqlalchemy as sa


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
