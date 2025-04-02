from app.service.entities.income_service import IncomeService
from tests.integration.service.factories import create_account
from .factories import create_income_payload
from nanoid import generate
import pytest


class TestIncomeServiceCase:
    """Test cases for IncomeService."""

    def test_create_income_service(self, default_account):
        """Test creating an income using IncomeService"""

        # Arrange: Given parameters for income creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the IncomeDomain
        payload = create_income_payload(account_id)
        fields = {
            "name",
            "amount",
            "max_yearly_growth_rate",
            "min_yearly_growth_rate",
            "start_age",
            "description",
            "end_age",
        }

        # Act: Call the service to create the income
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned IncomeDomain matches the input payload
        for field in fields:
            # Make sure each field in IncomeDomain matches the corresponding payload value
            assert (
                getattr(income_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            income_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            income_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_income_by_id_service(self, default_account):
        """Test retrieving an income by ID"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": income_id,
        }
        # Act: Retrieve the income by ID
        get_income_by_id_domain = IncomeService.get_income_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_income_by_id_domain.id == income_id
        assert get_income_by_id_domain == income_domain

    def test_get_incomes_service(self, default_account):
        """Test retrieving a list of incomes"""

        # Arrange: Get the initial count of incomes
        account_id = default_account.id
        original_income_count = len(IncomeService.get_incomes(account_id))

        # Arrange: Create multiple incomes
        new_income_count = 5
        created_incomes = [
            IncomeService.create_income(account_id, create_income_payload(account_id))
            for _ in range(new_income_count)
        ]

        # Act: Retrieve updated list of incomes
        incomes_from_service = IncomeService.get_incomes(account_id)
        updated_income_count = len(incomes_from_service)

        # Assert: Ensure each created income exists in the retrieved list
        assert all(exp in incomes_from_service for exp in created_incomes)

        # Assert: Ensure the total count has increased by the created number
        assert updated_income_count == original_income_count + new_income_count

    def test_update_income_service(self, default_account):
        """Test updating an income using IncomeService"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Income Service"

        updated_payload = {
            "id": income_id,
            "name": updated_name,
        }

        # Act: Update income through the service
        updated_income_domain = IncomeService.update_income(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the income is updated
        assert updated_income_domain.id == income_id
        assert updated_income_domain.name == updated_name

    def test_delete_income_by_id_service(self, default_account):
        """Test deleting an income by ID"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": income_id,
        }

        # Act: Delete the income
        IncomeService.delete_income_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted income will fail
        with pytest.raises(ValueError):
            IncomeService.get_income_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_income_service_owner_account_not_match(self, default_account):
        """Test creating an income when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for income creation
        payload = create_income_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            IncomeService.create_income(account_id=account_id, payload=payload)

    def test_get_income_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an income when owner and account are not match"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": income_id,
        }

        # Act: Retrieve the income by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            IncomeService.get_income_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_income_service_owner_account_not_match(self, default_account):
        """Test updating an income when owner and account are not match"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Income Service"

        updated_payload = {
            "id": income_id,
            "name": updated_name,
        }

        # Act: Retrieve the income by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            IncomeService.update_income(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_income_service_owner_account_not_match(self, default_account):
        """Test deleting an income when owner and account are not match"""

        # Arrange: Create an income first
        account_id = default_account.id
        payload = create_income_payload(account_id)
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": income_id,
        }

        # Act: Retrieve the income by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            IncomeService.delete_income_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_income_by_id_service_with_not_existed_income(self, default_account):
        """Test getting a not_existed income"""

        # Arrange: Generate an income id
        not_existed_income_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_income_id,
        }

        # Assert: Get income with invalid id should fail
        with pytest.raises(ValueError):
            IncomeService.get_income_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_income_service_with_not_existed_income(self, default_account):
        """Test updating a not_existed income"""

        # Arrange: Generate an income id
        not_existed_income_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Income Service"

        updated_payload = {
            "id": not_existed_income_id,
            "name": updated_name,
        }

        # Assert: Update income with invalid id should fail
        with pytest.raises(ValueError):
            IncomeService.update_income(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_income_service_with_not_existed_income(self, default_account):
        """Test deleting a not_existed income"""

        # Arrange: Generate an income id
        not_existed_income_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_income_id,
        }

        # Assert: Delete income with invalid id should fail
        with pytest.raises(ValueError):
            IncomeService.delete_income_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_income_service_with_invalid_field(self, default_account):
        """Test creating an income with invalid field using IncomeService"""

        # Arrange: Given parameters for income creation
        account_id = default_account.id
        payload = create_income_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for income creation
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(income_domain, invalid_field_name) is False

    def test_update_income_service_with_invalid_field(self, default_account):
        """Test updating an income with invalid field using IncomeService"""

        # Arrange: Given parameters for income creation
        account_id = default_account.id
        payload = create_income_payload(account_id)

        # Arrange: Given parameters for income creation
        income_domain = IncomeService.create_income(
            account_id=account_id, payload=payload
        )
        income_id = income_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Income Service"

        updated_payload = {
            "id": income_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the income by ID
        updated_income = IncomeService.update_income(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_income, invalid_field_name) is False

    def test_create_income_service_miss_required_field(self, default_account):
        """Test creating an income using IncomeService"""

        # Arrange: Given parameters for income creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the IncomeDomain
        payload = create_income_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create income when missing required field should raise ValueError
        with pytest.raises(ValueError):
            IncomeService.create_income(account_id=account_id, payload=payload)
