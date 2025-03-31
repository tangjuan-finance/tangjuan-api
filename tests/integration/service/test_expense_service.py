from app.service.expense_service import ExpenseService
from tests.integration.service.factories import create_expense_payload


class TestExpenseServiceCase:
    """Test cases for ExpenseService."""

    def test_create_expense_service(self, default_account):
        """Test creating an expense using ExpenseService"""

        # Arrange: Given parameters for expense creation
        account_id = default_account.id
        payload = create_expense_payload(account_id)

        # Arrange: Given parameters for expense creation
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned ExpenseDomain matches the input payload
        assert expense_domain.name == payload["name"]
        assert expense_domain.amount == payload["amount"]
        assert (
            expense_domain.max_yearly_growth_rate == payload["max_yearly_growth_rate"]
        )
        assert (
            expense_domain.min_yearly_growth_rate == payload["min_yearly_growth_rate"]
        )
        assert expense_domain.start_age == payload["start_age"]
        assert expense_domain.owner.id == payload["owner_id"]

    def test_get_expense_by_id_service(self, default_account):
        """Test retrieving an expense by ID"""

        # Arrange: Create an expense first
        account_id = default_account.id
        payload = create_expense_payload(account_id)
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )
        expense_id = expense_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": expense_id,
        }
        # Act: Retrieve the expense by ID
        get_expense_by_id_domain = ExpenseService.get_expense_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_expense_by_id_domain.id == expense_id
        assert get_expense_by_id_domain == expense_domain

    def test_get_expenses_service(self, default_account):
        """Test retrieving a list of expenses"""

        # Arrange: Get the initial count of expenses
        account_id = default_account.id
        original_expense_count = len(ExpenseService.get_expenses(account_id))

        # Arrange: Create multiple expenses
        new_expense_count = 5
        created_expenses = [
            ExpenseService.create_expense(
                account_id, create_expense_payload(account_id)
            )
            for _ in range(new_expense_count)
        ]

        # Act: Retrieve updated list of expenses
        expenses_from_service = ExpenseService.get_expenses(account_id)
        updated_expense_count = len(expenses_from_service)

        # Assert: Ensure each created expense exists in the retrieved list
        assert all(exp in expenses_from_service for exp in created_expenses)

        # Assert: Ensure the total count has increased by the created number
        assert updated_expense_count == original_expense_count + new_expense_count

    def test_update_expense_service(self, default_account):
        """Test updating an expense using ExpenseService"""

        # Arrange: Create an expense first
        account_id = default_account.id
        payload = create_expense_payload(account_id)
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )
        expense_id = expense_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Expense Service"

        updated_payload = {
            "id": expense_id,
            "name": updated_name,
        }

        # Act: Update expense through the service
        updated_expense_domain = ExpenseService.update_expense(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the expense is updated
        assert updated_expense_domain.id == expense_id
        assert updated_expense_domain.name == updated_name

    def test_delete_expense_by_id_service(self, default_account):
        """Test deleting an expense by ID"""

        # Arrange: Create an expense first
        account_id = default_account.id
        payload = create_expense_payload(account_id)
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )
        expense_id = expense_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": expense_id,
        }

        # Act: Delete the expense
        ExpenseService.delete_expense_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Act: Attempt to retrieve the deleted expense
        retrieved_expense = ExpenseService.get_expense_by_id(
            account_id=account_id, payload=delete_payload
        )

        # Assert: Ensure the expense is no longer retrievable
        assert retrieved_expense is None
