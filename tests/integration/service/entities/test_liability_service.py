from app.service.entities.liability_service import LiabilityService
from tests.factory import create_account
from .factories import create_liability_payload
from nanoid import generate
import pytest


class TestLiabilityServiceCase:
    """Test cases for LiabilityService."""

    def test_create_liability_service(self, default_account):
        """Test creating an liability using LiabilityService"""

        # Arrange: Given parameters for liability creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the LiabilityDomain
        payload = create_liability_payload(account_id)
        fields = {
            "name",
            "description",
            "principal_amount",
            "interest_rate",
            "start_age",
        }

        # Act: Call the service to create the liability
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned LiabilityDomain matches the input payload
        for field in fields:
            # Make sure each field in LiabilityDomain matches the corresponding payload value
            assert (
                getattr(liability_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            liability_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            liability_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_liability_by_id_service(self, default_account):
        """Test retrieving an liability by ID"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": liability_id,
        }
        # Act: Retrieve the liability by ID
        get_liability_by_id_domain = LiabilityService.get_liability_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_liability_by_id_domain.id == liability_id
        assert get_liability_by_id_domain == liability_domain

    def test_get_liabilities_service(self, default_account):
        """Test retrieving a list of liabilities"""

        # Arrange: Get the initial count of liabilities
        account_id = default_account.id
        original_liability_count = len(LiabilityService.get_liabilities(account_id))

        # Arrange: Create multiple liabilities
        new_liability_count = 5
        created_liabilities = [
            LiabilityService.create_liability(
                account_id, create_liability_payload(account_id)
            )
            for _ in range(new_liability_count)
        ]

        # Act: Retrieve updated list of liabilities
        liabilities_from_service = LiabilityService.get_liabilities(account_id)
        updated_liability_count = len(liabilities_from_service)

        # Assert: Ensure each created liability exists in the retrieved list
        assert all(exp in liabilities_from_service for exp in created_liabilities)

        # Assert: Ensure the total count has increased by the created number
        assert updated_liability_count == original_liability_count + new_liability_count

    def test_update_liability_service(self, default_account):
        """Test updating an liability using LiabilityService"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Liability Service"

        updated_payload = {
            "id": liability_id,
            "name": updated_name,
        }

        # Act: Update liability through the service
        updated_liability_domain = LiabilityService.update_liability(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the liability is updated
        assert updated_liability_domain.id == liability_id
        assert updated_liability_domain.name == updated_name

    def test_delete_liability_by_id_service(self, default_account):
        """Test deleting an liability by ID"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": liability_id,
        }

        # Act: Delete the liability
        LiabilityService.delete_liability_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted liability will fail
        with pytest.raises(ValueError):
            LiabilityService.get_liability_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_liability_service_owner_account_not_match(self, default_account):
        """Test creating an liability when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for liability creation
        payload = create_liability_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            LiabilityService.create_liability(account_id=account_id, payload=payload)

    def test_get_liability_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an liability when owner and account are not match"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": liability_id,
        }

        # Act: Retrieve the liability by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            LiabilityService.get_liability_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_liability_service_owner_account_not_match(self, default_account):
        """Test updating an liability when owner and account are not match"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Liability Service"

        updated_payload = {
            "id": liability_id,
            "name": updated_name,
        }

        # Act: Retrieve the liability by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            LiabilityService.update_liability(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_liability_service_owner_account_not_match(self, default_account):
        """Test deleting an liability when owner and account are not match"""

        # Arrange: Create an liability first
        account_id = default_account.id
        payload = create_liability_payload(account_id)
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": liability_id,
        }

        # Act: Retrieve the liability by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            LiabilityService.delete_liability_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_liability_by_id_service_with_not_existed_liability(
        self, default_account
    ):
        """Test getting a not_existed liability"""

        # Arrange: Generate an liability id
        not_existed_liability_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_liability_id,
        }

        # Assert: Get liability with invalid id should fail
        with pytest.raises(ValueError):
            LiabilityService.get_liability_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_liability_service_with_not_existed_liability(self, default_account):
        """Test updating a not_existed liability"""

        # Arrange: Generate an liability id
        not_existed_liability_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Liability Service"

        updated_payload = {
            "id": not_existed_liability_id,
            "name": updated_name,
        }

        # Assert: Update liability with invalid id should fail
        with pytest.raises(ValueError):
            LiabilityService.update_liability(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_liability_service_with_not_existed_liability(self, default_account):
        """Test deleting a not_existed liability"""

        # Arrange: Generate an liability id
        not_existed_liability_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_liability_id,
        }

        # Assert: Delete liability with invalid id should fail
        with pytest.raises(ValueError):
            LiabilityService.delete_liability_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_liability_service_with_invalid_field(self, default_account):
        """Test creating an liability with invalid field using LiabilityService"""

        # Arrange: Given parameters for liability creation
        account_id = default_account.id
        payload = create_liability_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for liability creation
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(liability_domain, invalid_field_name) is False

    def test_update_liability_service_with_invalid_field(self, default_account):
        """Test updating an liability with invalid field using LiabilityService"""

        # Arrange: Given parameters for liability creation
        account_id = default_account.id
        payload = create_liability_payload(account_id)

        # Arrange: Given parameters for liability creation
        liability_domain = LiabilityService.create_liability(
            account_id=account_id, payload=payload
        )
        liability_id = liability_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Liability Service"

        updated_payload = {
            "id": liability_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the liability by ID
        updated_liability = LiabilityService.update_liability(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_liability, invalid_field_name) is False

    def test_create_liability_service_miss_required_field(self, default_account):
        """Test creating an liability using LiabilityService"""

        # Arrange: Given parameters for liability creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the LiabilityDomain
        payload = create_liability_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create liability when missing required field should raise ValueError
        with pytest.raises(ValueError):
            LiabilityService.create_liability(account_id=account_id, payload=payload)
