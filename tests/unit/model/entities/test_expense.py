from app import db
from app.models import Expense
import sqlalchemy as sa
from .factories import create_entity


class TestExpenseModelCase:
    def test_create_expense(self, default_account):
        # Arrange
        name = "Default Expense"
        amount = 50000
        max_yearly_growth_rate = 0.5
        min_yearly_growth_rate = -0.5
        start_age = 20

        expense = create_entity(
            Expense,
            owner=default_account,
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
        )
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.name == Expense.name)
        )

        # Assert
        assert expense_from_db.amount == expense.amount
        assert expense_from_db.owner_id == expense.owner_id
