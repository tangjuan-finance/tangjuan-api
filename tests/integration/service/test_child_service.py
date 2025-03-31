from app.service.child_service import ChildService
from tests.integration.service.factories import create_child_payload, create_account
from nanoid import generate
import pytest


class TestChildServiceCase:
    """Test cases for ChildService."""

    def test_create_child_service(self, default_account):
        """Test creating an child using ChildService"""

        # Arrange: Given parameters for child creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ChildDomain
        payload = create_child_payload(account_id)
        fields = {
            "name",
            "birth_age",
            "description",
        }

        # Act: Call the service to create the child
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)

        # Assert: Ensure the returned ChildDomain matches the input payload
        for field in fields:
            # Make sure each field in ChildDomain matches the corresponding payload value
            assert (
                getattr(child_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            child_domain.parent.id == payload["parent_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the parent field in the domain matches the account_id
        assert (
            child_domain.parent.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_child_by_id_service(self, default_account):
        """Test retrieving an child by ID"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": child_id,
        }
        # Act: Retrieve the child by ID
        get_child_by_id_domain = ChildService.get_child_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_child_by_id_domain.id == child_id
        assert get_child_by_id_domain == child_domain

    def test_get_children_service(self, default_account):
        """Test retrieving a list of children"""

        # Arrange: Get the initial count of children
        account_id = default_account.id
        original_child_count = len(ChildService.get_children(account_id))

        # Arrange: Create multiple children
        new_child_count = 5
        created_children = [
            ChildService.create_child(account_id, create_child_payload(account_id))
            for _ in range(new_child_count)
        ]

        # Act: Retrieve updated list of children
        children_from_service = ChildService.get_children(account_id)
        updated_child_count = len(children_from_service)

        # Assert: Ensure each created child exists in the retrieved list
        assert all(exp in children_from_service for exp in created_children)

        # Assert: Ensure the total count has increased by the created number
        assert updated_child_count == original_child_count + new_child_count

    def test_update_child_service(self, default_account):
        """Test updating an child using ChildService"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Child Service"

        updated_payload = {
            "id": child_id,
            "name": updated_name,
        }

        # Act: Update child through the service
        updated_child_domain = ChildService.update_child(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the child is updated
        assert updated_child_domain.id == child_id
        assert updated_child_domain.name == updated_name

    def test_delete_child_by_id_service(self, default_account):
        """Test deleting an child by ID"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": child_id,
        }

        # Act: Delete the child
        ChildService.delete_child_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted child will fail
        with pytest.raises(ValueError):
            ChildService.get_child_by_id(account_id=account_id, payload=delete_payload)

    def test_create_child_service_parent_account_not_match(self, default_account):
        """Test creating an child when parent and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for child creation
        payload = create_child_payload(another_account_id)

        # Act: Given unmatch account_id and parent_id, it should raise Error

        with pytest.raises(PermissionError):
            ChildService.create_child(account_id=account_id, payload=payload)

    def test_get_child_by_id_service_parent_account_not_match(self, default_account):
        """Test getting an child when parent and account are not match"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": child_id,
        }

        # Act: Retrieve the child by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildService.get_child_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_child_service_parent_account_not_match(self, default_account):
        """Test updating an child when parent and account are not match"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Child Service"

        updated_payload = {
            "id": child_id,
            "name": updated_name,
        }

        # Act: Retrieve the child by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildService.update_child(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_child_service_parent_account_not_match(self, default_account):
        """Test deleting an child when parent and account are not match"""

        # Arrange: Create an child first
        account_id = default_account.id
        payload = create_child_payload(account_id)
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": child_id,
        }

        # Act: Retrieve the child by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildService.delete_child_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_child_by_id_service_with_not_existed_child(self, default_account):
        """Test getting a not_existed child"""

        # Arrange: Generate an child id
        not_existed_child_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_child_id,
        }

        # Assert: Get child with invalid id should fail
        with pytest.raises(ValueError):
            ChildService.get_child_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_child_service_with_not_existed_child(self, default_account):
        """Test updating a not_existed child"""

        # Arrange: Generate an child id
        not_existed_child_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Child Service"

        updated_payload = {
            "id": not_existed_child_id,
            "name": updated_name,
        }

        # Assert: Update child with invalid id should fail
        with pytest.raises(ValueError):
            ChildService.update_child(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_child_service_with_not_existed_child(self, default_account):
        """Test deleting a not_existed child"""

        # Arrange: Generate an child id
        not_existed_child_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_child_id,
        }

        # Assert: Delete child with invalid id should fail
        with pytest.raises(ValueError):
            ChildService.delete_child_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_child_service_with_invalid_field(self, default_account):
        """Test creating an child with invalid field using ChildService"""

        # Arrange: Given parameters for child creation
        account_id = default_account.id
        payload = create_child_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for child creation
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)

        # Assert: The invalid field is not added
        assert hasattr(child_domain, invalid_field_name) is False

    def test_update_child_service_with_invalid_field(self, default_account):
        """Test updating an child with invalid field using ChildService"""

        # Arrange: Given parameters for child creation
        account_id = default_account.id
        payload = create_child_payload(account_id)

        # Arrange: Given parameters for child creation
        child_domain = ChildService.create_child(account_id=account_id, payload=payload)
        child_id = child_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Child Service"

        updated_payload = {
            "id": child_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the child by ID
        updated_child = ChildService.update_child(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_child, invalid_field_name) is False

    def test_create_child_service_miss_required_field(self, default_account):
        """Test creating an child using ChildService"""

        # Arrange: Given parameters for child creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ChildDomain
        payload = create_child_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create child when missing required field should raise ValueError
        with pytest.raises(ValueError):
            ChildService.create_child(account_id=account_id, payload=payload)
