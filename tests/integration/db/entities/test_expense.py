from app import db
from app.infrastructure.models import Expense
import sqlalchemy as sa


class TestExpenseModelCase:
    def test_default_expense(self, default_expense):
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.id == default_expense.id)
        )

        # Assert
        assert expense_from_db.name == default_expense.name
        assert expense_from_db.amount == default_expense.amount
        assert (
            expense_from_db.max_yearly_growth_rate
            == default_expense.max_yearly_growth_rate
        )
        assert (
            expense_from_db.min_yearly_growth_rate
            == default_expense.min_yearly_growth_rate
        )
        assert expense_from_db.start_age == default_expense.start_age
        assert expense_from_db.created_at == default_expense.created_at
        assert expense_from_db.updated_at == default_expense.updated_at
        assert expense_from_db.owner_id == default_expense.owner_id
