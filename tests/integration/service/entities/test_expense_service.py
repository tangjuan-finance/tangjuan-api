from app.service.entities.expense_service import ExpenseService
from tests.integration.service.factories import create_account
from .factories import create_expense_payload
from nanoid import generate
import pytest


class TestExpenseServiceCase:
    """Test cases for ExpenseService."""

    def test_create_expense_service(self, default_account):
        """Test creating an expense using ExpenseService"""

        # Arrange: Given parameters for expense creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ExpenseDomain
        payload = create_expense_payload(account_id)
        fields = {
            "name",
            "amount",
            "max_yearly_growth_rate",
            "min_yearly_growth_rate",
            "start_age",
            "description",
            "end_age",
        }

        # Act: Call the service to create the expense
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned ExpenseDomain matches the input payload
        for field in fields:
            # Make sure each field in ExpenseDomain matches the corresponding payload value
            assert (
                getattr(expense_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            expense_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            expense_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

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

        # Assert: Attempt to retrieve the deleted expense will fail
        with pytest.raises(ValueError):
            ExpenseService.get_expense_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_expense_service_owner_account_not_match(self, default_account):
        """Test creating an expense when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for expense creation
        payload = create_expense_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            ExpenseService.create_expense(account_id=account_id, payload=payload)

    def test_get_expense_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an expense when owner and account are not match"""

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

        # Act: Retrieve the expense by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ExpenseService.get_expense_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_expense_service_owner_account_not_match(self, default_account):
        """Test updating an expense when owner and account are not match"""

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

        # Act: Retrieve the expense by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ExpenseService.update_expense(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_expense_service_owner_account_not_match(self, default_account):
        """Test deleting an expense when owner and account are not match"""

        # Arrange: Create an expense first
        account_id = default_account.id
        payload = create_expense_payload(account_id)
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )
        expense_id = expense_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": expense_id,
        }

        # Act: Retrieve the expense by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ExpenseService.delete_expense_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_expense_by_id_service_with_not_existed_expense(self, default_account):
        """Test getting a not_existed expense"""

        # Arrange: Generate an expense id
        not_existed_expense_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_expense_id,
        }

        # Assert: Get expense with invalid id should fail
        with pytest.raises(ValueError):
            ExpenseService.get_expense_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_expense_service_with_not_existed_expense(self, default_account):
        """Test updating a not_existed expense"""

        # Arrange: Generate an expense id
        not_existed_expense_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Expense Service"

        updated_payload = {
            "id": not_existed_expense_id,
            "name": updated_name,
        }

        # Assert: Update expense with invalid id should fail
        with pytest.raises(ValueError):
            ExpenseService.update_expense(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_expense_service_with_not_existed_expense(self, default_account):
        """Test deleting a not_existed expense"""

        # Arrange: Generate an expense id
        not_existed_expense_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_expense_id,
        }

        # Assert: Delete expense with invalid id should fail
        with pytest.raises(ValueError):
            ExpenseService.delete_expense_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_expense_service_with_invalid_field(self, default_account):
        """Test creating an expense with invalid field using ExpenseService"""

        # Arrange: Given parameters for expense creation
        account_id = default_account.id
        payload = create_expense_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for expense creation
        expense_domain = ExpenseService.create_expense(
            account_id=account_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(expense_domain, invalid_field_name) is False

    def test_update_expense_service_with_invalid_field(self, default_account):
        """Test updating an expense with invalid field using ExpenseService"""

        # Arrange: Given parameters for expense creation
        account_id = default_account.id
        payload = create_expense_payload(account_id)

        # Arrange: Given parameters for expense creation
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

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the expense by ID
        updated_expense = ExpenseService.update_expense(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_expense, invalid_field_name) is False

    def test_create_expense_service_miss_required_field(self, default_account):
        """Test creating an expense using ExpenseService"""

        # Arrange: Given parameters for expense creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ExpenseDomain
        payload = create_expense_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create expense when missing required field should raise ValueError
        with pytest.raises(ValueError):
            ExpenseService.create_expense(account_id=account_id, payload=payload)
