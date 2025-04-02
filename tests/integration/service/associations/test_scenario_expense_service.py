from app.service.associations import ScenarioExpenseService
from app.domain.entities import ExpenseDomain

# from tests.factory import create_account
from .factories import create_scenario_expense_payload
from tests.factory import create_expense

# from nanoid import generate
import pytest


class TestScenarioExpenseServiceCase:
    """Test cases for ScenarioExpenseService."""

    def test_create_scenario_expense_service(
        self, default_account, default_scenario_id, default_expense_id
    ):
        """Test creating an assoc using ScenarioExpenseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_expense_payload(
            scenario_id=default_scenario_id, expense_id=default_expense_id
        )

        # Act: Call the service to create the assoc
        response = ScenarioExpenseService.create_scenario_expense(
            account_id=account_id, payload=payload
        )

        assoc, expense = response.get("association"), response.get("expense")

        # Assert: Ensure the returned assoc matches the input payload
        for field in payload.keys():
            # Make sure each field in the assoc matches the corresponding payload value
            assert (
                getattr(assoc, field) == payload[field]
            ), f"Field {field} does not match expected value."

        # Assert: Check the return expense is the same as the given expense
        assert isinstance(expense, ExpenseDomain)
        assert expense.id == default_expense_id

    def test_get_expense_by_id_service(
        self, default_account, default_scenario_id, default_expense_id
    ):
        """Test retrieving an assoc by ID using ScenarioExpenseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_expense_payload(
            scenario_id=default_scenario_id, expense_id=default_expense_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioExpenseService.create_scenario_expense(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
            "expense_id": default_expense_id,
        }

        # Act: Retrieve the expense by ID
        response = ScenarioExpenseService.get_scenario_expense_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assoc, expense = response.get("association"), response.get("expense")

        # Assert: Check cid of assoc is as given
        assert assoc.scenario_id == default_scenario_id
        assert assoc.expense_id == default_expense_id

        # Assert: Check id of expense is as given
        assert expense.id == default_expense_id

    def test_get_expenses_service(self, default_account, default_scenario_id):
        """Test retrieving a list of Scenario Expense Assoc using ScenarioExpenseService"""

        # Arrange: Get the initial count of expenses
        account_id = default_account.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "scenario_id": default_scenario_id,
        }

        original_assocs_count = len(
            ScenarioExpenseService.get_scenario_expenses(
                account_id=account_id, payload=get_payload
            )
        )

        # Arrange: Create multiple assocs
        new_assoc_count = 5
        created_assocs = [
            ScenarioExpenseService.create_scenario_expense(
                account_id,
                create_scenario_expense_payload(
                    scenario_id=default_scenario_id,
                    expense_id=create_expense(default_account).id,
                ),
            ).get("association")
            for _ in range(new_assoc_count)
        ]
        # Act: Retrieve updated list of assocs
        assocs_from_service = [
            response["association"]
            for response in ScenarioExpenseService.get_scenario_expenses(
                account_id=account_id, payload=get_payload
            )
        ]
        updated_assocs_count = len(assocs_from_service)

        # Assert: Ensure each created expense exists in the retrieved list
        assert all(assoc in assocs_from_service for assoc in created_assocs)

        # Assert: Ensure the total count has increased by the created number
        assert updated_assocs_count == original_assocs_count + new_assoc_count

    def test_update_scenario_expense_service(
        self, default_account, default_scenario_id, default_expense_id
    ):
        """Test updating an assoc using ScenarioExpenseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_expense_payload(
            scenario_id=default_scenario_id, expense_id=default_expense_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioExpenseService.create_scenario_expense(
            account_id=account_id, payload=payload
        )

        # Arrange: Define updated parameters
        updated_memo = "Updated Assoc Memo"

        updated_payload = {
            "scenario_id": default_scenario_id,
            "expense_id": default_expense_id,
            "memo": updated_memo,
        }

        # Act: Update assoc through the service
        response = ScenarioExpenseService.update_scenario_expense(
            account_id=account_id, payload=updated_payload
        )
        assoc = response.get("association")

        # Assert: Ensure the assoc is updated
        assert assoc.scenario_id == default_scenario_id
        assert assoc.expense_id == default_expense_id
        assert assoc.memo == updated_memo

    def test_delete_expense_by_id_service(
        self, default_account, default_scenario_id, default_expense_id
    ):
        """Test deleting an assoc by ID using ScenarioExpenseService"""

        # Arrange: Extract account ID
        account_id = default_account.id

        # Arrange: Create the expected fields in the payload
        payload = create_scenario_expense_payload(
            scenario_id=default_scenario_id, expense_id=default_expense_id
        )

        # Arrange: Call the service to create the assoc
        ScenarioExpenseService.create_scenario_expense(
            account_id=account_id, payload=payload
        )

        # Arrange: Define payload for deletion
        delete_payload = {
            "scenario_id": default_scenario_id,
            "expense_id": default_expense_id,
        }

        # Act: Delete the expense
        ScenarioExpenseService.delete_scenario_expense_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted expense will fail
        with pytest.raises(ValueError):
            ScenarioExpenseService.get_scenario_expense_by_id(
                account_id=account_id, payload=delete_payload
            )

    # def test_create_scenario_expense_service_owner_account_not_match(
    #     self, default_account
    # ):
    #     """Test creating an expense when owner and account are not match"""

    #     account_id = default_account.id

    #     # Arrange: Create a different account
    #     another_account_id = create_account().id

    #     # Arrange: Given parameters for expense creation
    #     payload = create_expense_payload(another_account_id)

    #     # Act: Given unmatch account_id and owner_id, it should raise Error

    #     with pytest.raises(PermissionError):
    #         ExpenseService.create_expense(account_id=account_id, payload=payload)

    # def test_get_expense_by_id_service_owner_account_not_match(self, default_account):
    #     """Test getting an expense when owner and account are not match"""

    #     # Arrange: Create an expense first
    #     account_id = default_account.id
    #     payload = create_expense_payload(account_id)
    #     expense_domain = ExpenseService.create_expense(
    #         account_id=account_id, payload=payload
    #     )
    #     expense_id = expense_domain.id

    #     # Arrange: Define payload for retrieval
    #     get_payload = {
    #         "id": expense_id,
    #     }

    #     # Act: Retrieve the expense by ID with different account ID
    #     another_account_id = create_account().id

    #     with pytest.raises(PermissionError):
    #         ExpenseService.get_expense_by_id(
    #             account_id=another_account_id,
    #             payload=get_payload,
    #         )

    # def test_update_scenario_expense_service_owner_account_not_match(
    #     self, default_account
    # ):
    #     """Test updating an expense when owner and account are not match"""

    #     # Arrange: Create an expense first
    #     account_id = default_account.id
    #     payload = create_expense_payload(account_id)
    #     expense_domain = ExpenseService.create_expense(
    #         account_id=account_id, payload=payload
    #     )
    #     expense_id = expense_domain.id

    #     # Arrange: Define updated parameters
    #     updated_name = "Updated Expense Service"

    #     updated_payload = {
    #         "id": expense_id,
    #         "name": updated_name,
    #     }

    #     # Act: Retrieve the expense by ID with different account ID
    #     another_account_id = create_account().id

    #     with pytest.raises(PermissionError):
    #         ExpenseService.update_expense(
    #             account_id=another_account_id, payload=updated_payload
    #         )

    # def test_delete_scenario_expense_service_owner_account_not_match(
    #     self, default_account
    # ):
    #     """Test deleting an expense when owner and account are not match"""

    #     # Arrange: Create an expense first
    #     account_id = default_account.id
    #     payload = create_expense_payload(account_id)
    #     expense_domain = ExpenseService.create_expense(
    #         account_id=account_id, payload=payload
    #     )
    #     expense_id = expense_domain.id

    #     # Arrange: Define payload for retrieval
    #     delete_payload = {
    #         "id": expense_id,
    #     }

    #     # Act: Retrieve the expense by ID with different account ID
    #     another_account_id = create_account().id

    #     with pytest.raises(PermissionError):
    #         ExpenseService.delete_expense_by_id(
    #             account_id=another_account_id, payload=delete_payload
    #         )

    # def test_get_expense_by_id_service_with_not_existed_expense(self, default_account):
    #     """Test getting a not_existed expense"""

    #     # Arrange: Generate an expense id
    #     not_existed_expense_id = generate(size=13)

    #     # Arrange: Define payload for retrieval
    #     get_payload = {
    #         "id": not_existed_expense_id,
    #     }

    #     # Assert: Get expense with invalid id should fail
    #     with pytest.raises(ValueError):
    #         ExpenseService.get_expense_by_id(
    #             account_id=default_account.id,
    #             payload=get_payload,
    #         )

    # def test_update_scenario_expense_service_with_not_existed_expense(
    #     self, default_account
    # ):
    #     """Test updating a not_existed expense"""

    #     # Arrange: Generate an expense id
    #     not_existed_expense_id = generate(size=13)

    #     # Arrange: Define updated parameters
    #     updated_name = "Updated Expense Service"

    #     updated_payload = {
    #         "id": not_existed_expense_id,
    #         "name": updated_name,
    #     }

    #     # Assert: Update expense with invalid id should fail
    #     with pytest.raises(ValueError):
    #         ExpenseService.update_expense(
    #             account_id=default_account.id, payload=updated_payload
    #         )

    # def test_delete_scenario_expense_service_with_not_existed_expense(
    #     self, default_account
    # ):
    #     """Test deleting a not_existed expense"""

    #     # Arrange: Generate an expense id
    #     not_existed_expense_id = generate(size=13)

    #     # Arrange: Define payload for retrieval
    #     delete_payload = {
    #         "id": not_existed_expense_id,
    #     }

    #     # Assert: Delete expense with invalid id should fail
    #     with pytest.raises(ValueError):
    #         ExpenseService.delete_expense_by_id(
    #             account_id=default_account.id, payload=delete_payload
    #         )

    # def test_create_scenario_expense_service_with_invalid_field(self, default_account):
    #     """Test creating an expense with invalid field using ExpenseService"""

    #     # Arrange: Given parameters for expense creation
    #     account_id = default_account.id
    #     payload = create_expense_payload(account_id)

    #     # Arrange: Add an invalid field
    #     invalid_field_name = "invalid_field"
    #     payload[invalid_field_name] = "this field is invalid"

    #     # Arrange: Given parameters for expense creation
    #     expense_domain = ExpenseService.create_expense(
    #         account_id=account_id, payload=payload
    #     )

    #     # Assert: The invalid field is not added
    #     assert hasattr(expense_domain, invalid_field_name) is False

    # def test_update_scenario_expense_service_with_invalid_field(self, default_account):
    #     """Test updating an expense with invalid field using ExpenseService"""

    #     # Arrange: Given parameters for expense creation
    #     account_id = default_account.id
    #     payload = create_expense_payload(account_id)

    #     # Arrange: Given parameters for expense creation
    #     expense_domain = ExpenseService.create_expense(
    #         account_id=account_id, payload=payload
    #     )
    #     expense_id = expense_domain.id

    #     # Arrange: Define updated parameters
    #     updated_name = "Updated Expense Service"

    #     updated_payload = {
    #         "id": expense_id,
    #         "name": updated_name,
    #     }

    #     # Arrange: Add an invalid field
    #     invalid_field_name = "invalid_field"
    #     updated_payload[invalid_field_name] = "this field is invalid"

    #     # Act: Retrieve the expense by ID
    #     updated_expense = ExpenseService.update_expense(
    #         account_id=account_id, payload=updated_payload
    #     )

    #     assert hasattr(updated_expense, invalid_field_name) is False

    # def test_create_scenario_expense_service_miss_required_field(self, default_account):
    #     """Test creating an expense using ExpenseService"""

    #     # Arrange: Given parameters for expense creation
    #     account_id = default_account.id

    #     # Arrange: Define the expected fields that should be part of the ExpenseDomain
    #     payload = create_expense_payload(account_id)

    #     # Arrange: Remove required field
    #     del payload["name"]

    #     # Assert: Create expense when missing required field should raise ValueError
    #     with pytest.raises(ValueError):
    #         ExpenseService.create_expense(account_id=account_id, payload=payload)
