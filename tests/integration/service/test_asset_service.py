from app.service.asset_service import AssetService
from tests.integration.service.factories import create_asset_payload, create_account
from nanoid import generate
import pytest


class TestAssetServiceCase:
    """Test cases for AssetService."""

    def test_create_asset_service(self, default_account):
        """Test creating an asset using AssetService"""

        # Arrange: Given parameters for asset creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the AssetDomain
        payload = create_asset_payload(account_id)
        fields = {
            "name",
            "amount",
            "max_yearly_return_rate",
            "min_yearly_return_rate",
            "start_age",
            "description",
            "end_age",
        }

        # Act: Call the service to create the asset
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)

        # Assert: Ensure the returned AssetDomain matches the input payload
        for field in fields:
            # Make sure each field in AssetDomain matches the corresponding payload value
            assert (
                getattr(asset_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            asset_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            asset_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_asset_by_id_service(self, default_account):
        """Test retrieving an asset by ID"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": asset_id,
        }
        # Act: Retrieve the asset by ID
        get_asset_by_id_domain = AssetService.get_asset_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_asset_by_id_domain.id == asset_id
        assert get_asset_by_id_domain == asset_domain

    def test_get_assets_service(self, default_account):
        """Test retrieving a list of assets"""

        # Arrange: Get the initial count of assets
        account_id = default_account.id
        original_asset_count = len(AssetService.get_assets(account_id))

        # Arrange: Create multiple assets
        new_asset_count = 5
        created_assets = [
            AssetService.create_asset(account_id, create_asset_payload(account_id))
            for _ in range(new_asset_count)
        ]

        # Act: Retrieve updated list of assets
        assets_from_service = AssetService.get_assets(account_id)
        updated_asset_count = len(assets_from_service)

        # Assert: Ensure each created asset exists in the retrieved list
        assert all(exp in assets_from_service for exp in created_assets)

        # Assert: Ensure the total count has increased by the created number
        assert updated_asset_count == original_asset_count + new_asset_count

    def test_update_asset_service(self, default_account):
        """Test updating an asset using AssetService"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Asset Service"

        updated_payload = {
            "id": asset_id,
            "name": updated_name,
        }

        # Act: Update asset through the service
        updated_asset_domain = AssetService.update_asset(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the asset is updated
        assert updated_asset_domain.id == asset_id
        assert updated_asset_domain.name == updated_name

    def test_delete_asset_by_id_service(self, default_account):
        """Test deleting an asset by ID"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": asset_id,
        }

        # Act: Delete the asset
        AssetService.delete_asset_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted asset will fail
        with pytest.raises(ValueError):
            AssetService.get_asset_by_id(account_id=account_id, payload=delete_payload)

    def test_create_asset_service_owner_account_not_match(self, default_account):
        """Test creating an asset when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for asset creation
        payload = create_asset_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            AssetService.create_asset(account_id=account_id, payload=payload)

    def test_get_asset_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an asset when owner and account are not match"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": asset_id,
        }

        # Act: Retrieve the asset by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            AssetService.get_asset_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_asset_service_owner_account_not_match(self, default_account):
        """Test updating an asset when owner and account are not match"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Asset Service"

        updated_payload = {
            "id": asset_id,
            "name": updated_name,
        }

        # Act: Retrieve the asset by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            AssetService.update_asset(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_asset_service_owner_account_not_match(self, default_account):
        """Test deleting an asset when owner and account are not match"""

        # Arrange: Create an asset first
        account_id = default_account.id
        payload = create_asset_payload(account_id)
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": asset_id,
        }

        # Act: Retrieve the asset by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            AssetService.delete_asset_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_asset_by_id_service_with_not_existed_asset(self, default_account):
        """Test getting a not_existed asset"""

        # Arrange: Generate an asset id
        not_existed_asset_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_asset_id,
        }

        # Assert: Get asset with invalid id should fail
        with pytest.raises(ValueError):
            AssetService.get_asset_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_asset_service_with_not_existed_asset(self, default_account):
        """Test updating a not_existed asset"""

        # Arrange: Generate an asset id
        not_existed_asset_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Asset Service"

        updated_payload = {
            "id": not_existed_asset_id,
            "name": updated_name,
        }

        # Assert: Update asset with invalid id should fail
        with pytest.raises(ValueError):
            AssetService.update_asset(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_asset_service_with_not_existed_asset(self, default_account):
        """Test deleting a not_existed asset"""

        # Arrange: Generate an asset id
        not_existed_asset_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_asset_id,
        }

        # Assert: Delete asset with invalid id should fail
        with pytest.raises(ValueError):
            AssetService.delete_asset_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_asset_service_with_invalid_field(self, default_account):
        """Test creating an asset with invalid field using AssetService"""

        # Arrange: Given parameters for asset creation
        account_id = default_account.id
        payload = create_asset_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for asset creation
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)

        # Assert: The invalid field is not added
        assert hasattr(asset_domain, invalid_field_name) is False

    def test_update_asset_service_with_invalid_field(self, default_account):
        """Test updating an asset with invalid field using AssetService"""

        # Arrange: Given parameters for asset creation
        account_id = default_account.id
        payload = create_asset_payload(account_id)

        # Arrange: Given parameters for asset creation
        asset_domain = AssetService.create_asset(account_id=account_id, payload=payload)
        asset_id = asset_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Asset Service"

        updated_payload = {
            "id": asset_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the asset by ID
        updated_asset = AssetService.update_asset(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_asset, invalid_field_name) is False

    def test_create_asset_service_miss_required_field(self, default_account):
        """Test creating an asset using AssetService"""

        # Arrange: Given parameters for asset creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the AssetDomain
        payload = create_asset_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create asset when missing required field should raise ValueError
        with pytest.raises(ValueError):
            AssetService.create_asset(account_id=account_id, payload=payload)
