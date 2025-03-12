from app import db
from app.models import Child
import sqlalchemy as sa
from .factories import create_entity


class TestChildModelCase:
    def test_create_child(self, default_user):
        # Arrange
        name = "Default Child"
        birth_age = 34
        independent_age = 56

        child = create_entity(
            Child,
            parent_id=default_user,
            name=name,
            birth_age=birth_age,
            independent_age=independent_age,
        )
        # Act
        child_from_db = db.session.scalar(
            sa.select(Child).where(Child.name == Child.name)
        )

        # Assert
        assert child_from_db.birth_age == child.birth_age
        assert child_from_db.owner_id == child.owner_id
