from app import db
from app.models import Expense
import sqlalchemy as sa
from .factories import create_entity
# from tests.constants import MAX_BIGINT
# from hypothesis import given, strategies as st


class TestExpenseModelCase:
    # @given(name=st.text(min_size=1, max_size=128), \
    #     amount=st.integers(max_value=MAX_BIGINT), \
    #     description=st.text(max_size=0),\
    #     # max_yearly_growth_rate=st.decimals(min_value=-100,max_value=100),\
    #     # min_yearly_growth_rate=st.decimals(min_value=-100,max_value=100),
    #     start_age=st.integers(min_value=0,max_value=200),\
    #     end_age=st.integers(min_value=0,max_value=200),\
    #     )
    # def test_create_expense(self, default_user, name, amount, description, \
    #                         max_yearly_growth_rate, min_yearly_growth_rate, \
    #                             start_age, end_age, created_at):
    def test_create_expense(self, default_user):
        # Arrange
        name = "Default Expense"
        amount = 50000
        description = "This is cool!"
        start_year = 20
        end_year = 50

        expense = create_entity(
            Expense,
            owner=default_user,
            name=name,
            amount=amount,
            description=description,
            start_year=start_year,
            end_year=end_year,
        )
        # Act
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.name == Expense.name)
        )

        # Assert
        assert expense_from_db.amount == expense.amount
        assert expense_from_db.owner_id == expense.owner_id
