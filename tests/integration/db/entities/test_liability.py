from app import db
from app.infrastructure.models import Liability
import sqlalchemy as sa


class TestLiabilityModelCase:
    def test_default_liability(self, default_liability):
        # Act
        liability_from_db = db.session.scalar(
            sa.select(Liability).where(Liability.id == default_liability.id)
        )

        # Assert
        assert liability_from_db.name == default_liability.name
        assert liability_from_db.principal_amount == default_liability.principal_amount
        assert liability_from_db.interest_rate == default_liability.interest_rate
        assert liability_from_db.start_age == default_liability.start_age
        assert liability_from_db.end_age == default_liability.end_age
        assert liability_from_db.created_at == default_liability.created_at
        assert liability_from_db.updated_at == default_liability.updated_at
        assert liability_from_db.owner_id == default_liability.owner_id
