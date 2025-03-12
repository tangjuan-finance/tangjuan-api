from app import db
from app.models import House
import sqlalchemy as sa
from .factories import create_entity


class TestHouseModelCase:
    def test_create_house(self, default_user):
        # Arrange
        name = "Default House"
        amount = 20000000
        down_payment = 3000000
        interest_rate = 3.0
        loan_term = 40
        purchase_age = 20

        house = create_entity(
            House,
            owner=default_user,
            name=name,
            amount=amount,
            down_payment=down_payment,
            interest_rate=interest_rate,
            loan_term=loan_term,
            purchase_age=purchase_age,
        )
        # Act
        house_from_db = db.session.scalar(
            sa.select(House).where(House.name == House.name)
        )

        # Assert
        assert house_from_db.amount == house.amount
        assert house_from_db.owner_id == house.owner_id
