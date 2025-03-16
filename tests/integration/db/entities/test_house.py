from app import db
from app.infrastructure.models import House
import sqlalchemy as sa


class TestHouseModelCase:
    def test_default_house(self, default_house):
        # Act
        house_from_db = db.session.scalar(
            sa.select(House).where(House.id == default_house.id)
        )

        # Assert
        assert house_from_db.name == default_house.name
        assert house_from_db.amount == default_house.amount
        assert house_from_db.down_payment == default_house.down_payment
        assert house_from_db.interest_rate == default_house.interest_rate
        assert house_from_db.loan_term == default_house.loan_term
        assert house_from_db.purchase_age == default_house.purchase_age
        assert house_from_db.created_at == default_house.created_at
        assert house_from_db.updated_at == default_house.updated_at
        assert house_from_db.owner_id == default_house.owner_id
