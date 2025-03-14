from app import db
from app.models import Income
import sqlalchemy as sa
from .factories import create_entity


class TestIncomeModelCase:
    def test_create_income(self, default_account):
        # Arrange
        name = "Default Income"
        amount = 50000
        max_yearly_growth_rate = 0.5
        min_yearly_growth_rate = -0.5
        start_age = 20

        income = create_entity(
            Income,
            owner=default_account,
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
        )
        # Act
        income_from_db = db.session.scalar(
            sa.select(Income).where(Income.name == Income.name)
        )

        # Assert
        assert income_from_db.amount == income.amount
        assert income_from_db.owner_id == income.owner_id
