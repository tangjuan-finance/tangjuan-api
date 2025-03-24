from app.repository.entities import ExpenseRepo
from app.infrastructure.models.entities import Expense
from tests.unit.factories import ExpenseDomainFactory
import sqlalchemy as sa
from app import db


class TestExpenseRepoCase:
    def test_create_expense_domain_through_repo(self):
        # Arrange: Create an expense domain using the factory
        expense = ExpenseDomainFactory()

        # Act: Save the expense domain using the repo and return the saved entity
        expense_from_repo = ExpenseRepo.create(expense)
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.id == expense.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert expense_from_repo.id == expense_from_db.id
        assert expense_from_repo.name == expense_from_db.name
        assert expense_from_repo.amount == expense_from_db.amount
        assert (
            expense_from_repo.max_yearly_growth_rate
            == expense_from_db.max_yearly_growth_rate
        )
        assert (
            expense_from_repo.min_yearly_growth_rate
            == expense_from_db.min_yearly_growth_rate
        )
        assert expense_from_repo.start_age == expense_from_db.start_age
        assert expense_from_repo.owner == expense_from_db.owner
        assert expense_from_repo.created_at == expense_from_db.created_at
        assert expense_from_repo.updated_at == expense_from_db.updated_at

    def test_update_expense_domain_through_repo(self):
        # Arrange: Create an expense domain using the factory
        expense = ExpenseDomainFactory()
        expense_from_repo = ExpenseRepo.create(expense)
        updated_name = "Updated Expense Domain"

        # Act: Update the expense domain object (before saving)
        expense_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_expense = ExpenseRepo.save(expense_from_repo)

        # Query the database to verify the updated expense record
        expense_from_db = db.session.scalar(
            sa.select(Expense).where(Expense.id == expense_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_expense.id == expense_from_db.id
        assert updated_expense.name == expense_from_db.name
        assert updated_expense.created_at == expense_from_db.created_at
        assert updated_expense.updated_at != expense_from_db.updated_at

    def test_get_expense_domain_by_id_through_repo(self):
        # Arrange: Create an expense domain using the factory
        expense = ExpenseDomainFactory()
        ExpenseRepo.create(expense)

        # Act: Update the expense domain object (before saving)
        expense_get_by_id = ExpenseRepo.get_by_id(expense.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert expense_get_by_id.id == expense.id
        assert expense_get_by_id.name == expense.name

    def test_get_expense_domain_list_through_repo(self):
        # Arrange: Create an expense domain using the factory
        origin_expense_list_length = len(ExpenseRepo.get_list())

        # Act: Create 5 new expense domains
        for _ in range(5):
            expense = ExpenseDomainFactory()
            ExpenseRepo.create(expense)

        # Assert: Ensure the list length is increased by 5
        updated_expense_list_length = len(ExpenseRepo.get_list())
        assert updated_expense_list_length == (origin_expense_list_length + 5)

    def test_delete_expense_domain_through_repo(self):
        # Arrange: Create an expense domain using the factory
        expense = ExpenseDomainFactory()
        expense_from_repo = ExpenseRepo.create(expense)

        # Act: Delete the expense domain object
        ExpenseRepo.delete(expense_from_repo)

        # Assert: Ensure the expense record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(Expense).where(Expense.id == expense_from_repo.id)
            )
            is None
        )
