from app import db
from app.infrastructure.models import Income
import sqlalchemy as sa


class TestIncomeModelCase:
    def test_default_income(self, default_income):
        # Act
        income_from_db = db.session.scalar(
            sa.select(Income).where(Income.id == default_income.id)
        )

        # Assert
        assert income_from_db.name == default_income.name
        assert income_from_db.amount == default_income.amount
        assert (
            income_from_db.max_yearly_growth_rate
            == default_income.max_yearly_growth_rate
        )
        assert (
            income_from_db.min_yearly_growth_rate
            == default_income.min_yearly_growth_rate
        )
        assert income_from_db.start_age == default_income.start_age
        assert income_from_db.end_age == default_income.end_age
        assert income_from_db.created_at == default_income.created_at
        assert income_from_db.updated_at == default_income.updated_at
        assert income_from_db.owner_id == default_income.owner_id
