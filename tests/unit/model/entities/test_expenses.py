from app import db
from app.models import Expense
import sqlalchemy as sa
from .factories import create_user, create_entity


class TestExpenseModelCase:
    def test_create_expense(self):
        # Arrange
        owner = create_user()
        expense = create_entity(
            Expense, owner=owner, start_year=30, name="Good Job", amount=50000
        )
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.name == Expense.name)
        )

        # Assert
        assert expense_from_db.amount == expense.amount
        assert expense_from_db.owner_id == expense.owner_id
