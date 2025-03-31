from app.service.house_service import HouseService
from tests.integration.service.factories import create_house_payload, create_account
from nanoid import generate
import pytest


class TestHouseServiceCase:
    """Test cases for HouseService."""

    def test_create_house_service(self, default_account):
        """Test creating an house using HouseService"""

        # Arrange: Given parameters for house creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the HouseDomain
        payload = create_house_payload(account_id)
        fields = {
            "name",
            "amount",
            "down_payment",
            "interest_rate",
            "loan_term",
            "purchase_age",
            "description",
            "sale_age",
        }

        # Act: Call the service to create the house
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)

        # Assert: Ensure the returned HouseDomain matches the input payload
        for field in fields:
            # Make sure each field in HouseDomain matches the corresponding payload value
            assert (
                getattr(house_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            house_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            house_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_house_by_id_service(self, default_account):
        """Test retrieving an house by ID"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": house_id,
        }
        # Act: Retrieve the house by ID
        get_house_by_id_domain = HouseService.get_house_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_house_by_id_domain.id == house_id
        assert get_house_by_id_domain == house_domain

    def test_get_houses_service(self, default_account):
        """Test retrieving a list of houses"""

        # Arrange: Get the initial count of houses
        account_id = default_account.id
        original_house_count = len(HouseService.get_houses(account_id))

        # Arrange: Create multiple houses
        new_house_count = 5
        created_houses = [
            HouseService.create_house(account_id, create_house_payload(account_id))
            for _ in range(new_house_count)
        ]

        # Act: Retrieve updated list of houses
        houses_from_service = HouseService.get_houses(account_id)
        updated_house_count = len(houses_from_service)

        # Assert: Ensure each created house exists in the retrieved list
        assert all(exp in houses_from_service for exp in created_houses)

        # Assert: Ensure the total count has increased by the created number
        assert updated_house_count == original_house_count + new_house_count

    def test_update_house_service(self, default_account):
        """Test updating an house using HouseService"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated House Service"

        updated_payload = {
            "id": house_id,
            "name": updated_name,
        }

        # Act: Update house through the service
        updated_house_domain = HouseService.update_house(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the house is updated
        assert updated_house_domain.id == house_id
        assert updated_house_domain.name == updated_name

    def test_delete_house_by_id_service(self, default_account):
        """Test deleting an house by ID"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": house_id,
        }

        # Act: Delete the house
        HouseService.delete_house_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted house will fail
        with pytest.raises(ValueError):
            HouseService.get_house_by_id(account_id=account_id, payload=delete_payload)

    def test_create_house_service_owner_account_not_match(self, default_account):
        """Test creating an house when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for house creation
        payload = create_house_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            HouseService.create_house(account_id=account_id, payload=payload)

    def test_get_house_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an house when owner and account are not match"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": house_id,
        }

        # Act: Retrieve the house by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            HouseService.get_house_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_house_service_owner_account_not_match(self, default_account):
        """Test updating an house when owner and account are not match"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated House Service"

        updated_payload = {
            "id": house_id,
            "name": updated_name,
        }

        # Act: Retrieve the house by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            HouseService.update_house(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_house_service_owner_account_not_match(self, default_account):
        """Test deleting an house when owner and account are not match"""

        # Arrange: Create an house first
        account_id = default_account.id
        payload = create_house_payload(account_id)
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": house_id,
        }

        # Act: Retrieve the house by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            HouseService.delete_house_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_house_by_id_service_with_not_existed_house(self, default_account):
        """Test getting a not_existed house"""

        # Arrange: Generate an house id
        not_existed_house_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_house_id,
        }

        # Assert: Get house with invalid id should fail
        with pytest.raises(ValueError):
            HouseService.get_house_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_house_service_with_not_existed_house(self, default_account):
        """Test updating a not_existed house"""

        # Arrange: Generate an house id
        not_existed_house_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated House Service"

        updated_payload = {
            "id": not_existed_house_id,
            "name": updated_name,
        }

        # Assert: Update house with invalid id should fail
        with pytest.raises(ValueError):
            HouseService.update_house(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_house_service_with_not_existed_house(self, default_account):
        """Test deleting a not_existed house"""

        # Arrange: Generate an house id
        not_existed_house_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_house_id,
        }

        # Assert: Delete house with invalid id should fail
        with pytest.raises(ValueError):
            HouseService.delete_house_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_house_service_with_invalid_field(self, default_account):
        """Test creating an house with invalid field using HouseService"""

        # Arrange: Given parameters for house creation
        account_id = default_account.id
        payload = create_house_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for house creation
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)

        # Assert: The invalid field is not added
        assert hasattr(house_domain, invalid_field_name) is False

    def test_update_house_service_with_invalid_field(self, default_account):
        """Test updating an house with invalid field using HouseService"""

        # Arrange: Given parameters for house creation
        account_id = default_account.id
        payload = create_house_payload(account_id)

        # Arrange: Given parameters for house creation
        house_domain = HouseService.create_house(account_id=account_id, payload=payload)
        house_id = house_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated House Service"

        updated_payload = {
            "id": house_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the house by ID
        updated_house = HouseService.update_house(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_house, invalid_field_name) is False

    def test_create_house_service_miss_required_field(self, default_account):
        """Test creating an house using HouseService"""

        # Arrange: Given parameters for house creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the HouseDomain
        payload = create_house_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create house when missing required field should raise ValueError
        with pytest.raises(ValueError):
            HouseService.create_house(account_id=account_id, payload=payload)
