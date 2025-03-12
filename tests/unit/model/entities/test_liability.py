from app import db
from app.models import Liability
import sqlalchemy as sa
from .factories import create_entity


class TestLiabilityModelCase:
    def test_create_liability(self, default_user):
        # Arrange
        name = "Default Liability"
        principal_amount = 50000
        interest_rate = 0.5
        start_age = 20
        end_age = 50

        liability = create_entity(
            Liability,
            owner=default_user,
            name=name,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            start_age=start_age,
            end_age=end_age,
        )
        # Act
        liability_from_db = db.session.scalar(
            sa.select(Liability).where(Liability.name == Liability.name)
        )

        # Assert
        assert liability_from_db.principal_amount == liability.principal_amount
        assert liability_from_db.owner_id == liability.owner_id
