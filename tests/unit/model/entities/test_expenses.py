from app import db
from app.models import Expense
import sqlalchemy as sa
from .factories import create_entity
# from hypothesis import given, strategies as st


# @given(name=st.text(max_size=120), amount=st.integers)
class TestExpenseModelCase:
    def test_create_expense(self, default_user):
        # Arrange
        expense = create_entity(
            Expense,
            owner=default_user,
            name="Good Expense",
            start_year=30,
            amount=50000,
        )
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.name == Expense.name)
        )

        # Assert
        assert expense_from_db.amount == expense.amount
        assert expense_from_db.owner_id == expense.owner_id
