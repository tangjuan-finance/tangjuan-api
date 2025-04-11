from app import db
from app.infrastructure.models import Risk
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
        assert risk_from_db.amount == default_risk.amount
        assert risk_from_db.probability == default_risk.probability
        assert risk_from_db.start_age == default_risk.start_age
        assert risk_from_db.end_age == default_risk.end_age
        assert risk_from_db.created_at == default_risk.created_at
        assert risk_from_db.updated_at == default_risk.updated_at
        assert risk_from_db.owner_id == default_risk.owner_id
