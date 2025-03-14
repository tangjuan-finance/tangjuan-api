from app import db
from app.models import Risk
import sqlalchemy as sa
from .factories import create_entity


class TestRiskModelCase:
    def test_create_risk(self, default_account):
        # Arrange
        name = "Default Risk"
        principal_amount = 50000
        interest_rate = 0.5
        start_age = 20
        end_age = 50

        risk = create_entity(
            Risk,
            owner=default_account,
            name=name,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            start_age=start_age,
            end_age=end_age,
        )
        # Act
        risk_from_db = db.session.scalar(sa.select(Risk).where(Risk.name == Risk.name))

        # Assert
        assert risk_from_db.principal_amount == risk.principal_amount
        assert risk_from_db.owner_id == risk.owner_id
