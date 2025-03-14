from app import db
from app.models import Risk
import sqlalchemy as sa


class TestRiskModelCase:
    def test_default_risk(self, default_risk):
        # Arrange

        # Act
        risk_from_db = db.session.scalar(
            sa.select(Risk).where(Risk.id == default_risk.id)
        )

        # Assert
        assert risk_from_db.name == default_risk.name
        assert risk_from_db.principal_amount == default_risk.principal_amount
        assert risk_from_db.interest_rate == default_risk.interest_rate
        assert risk_from_db.start_age == default_risk.start_age
        assert risk_from_db.end_age == default_risk.end_age
        assert risk_from_db.owner_id == default_risk.owner_id
