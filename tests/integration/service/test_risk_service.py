from app.service.risk_service import RiskService
from tests.integration.service.factories import create_risk_payload, create_account
from nanoid import generate
import pytest


class TestRiskServiceCase:
    """Test cases for RiskService."""

    def test_create_risk_service(self, default_account):
        """Test creating an risk using RiskService"""

        # Arrange: Given parameters for risk creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the RiskDomain
        payload = create_risk_payload(account_id)
        fields = {
            "name",
            "description",
            "min_loss",
            "start_age",
        }

        # Act: Call the service to create the risk
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)

        # Assert: Ensure the returned RiskDomain matches the input payload
        for field in fields:
            # Make sure each field in RiskDomain matches the corresponding payload value
            assert (
                getattr(risk_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            risk_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            risk_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_risk_by_id_service(self, default_account):
        """Test retrieving an risk by ID"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": risk_id,
        }
        # Act: Retrieve the risk by ID
        get_risk_by_id_domain = RiskService.get_risk_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_risk_by_id_domain.id == risk_id
        assert get_risk_by_id_domain == risk_domain

    def test_get_risks_service(self, default_account):
        """Test retrieving a list of risks"""

        # Arrange: Get the initial count of risks
        account_id = default_account.id
        original_risk_count = len(RiskService.get_risks(account_id))

        # Arrange: Create multiple risks
        new_risk_count = 5
        created_risks = [
            RiskService.create_risk(account_id, create_risk_payload(account_id))
            for _ in range(new_risk_count)
        ]

        # Act: Retrieve updated list of risks
        risks_from_service = RiskService.get_risks(account_id)
        updated_risk_count = len(risks_from_service)

        # Assert: Ensure each created risk exists in the retrieved list
        assert all(exp in risks_from_service for exp in created_risks)

        # Assert: Ensure the total count has increased by the created number
        assert updated_risk_count == original_risk_count + new_risk_count

    def test_update_risk_service(self, default_account):
        """Test updating an risk using RiskService"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Risk Service"

        updated_payload = {
            "id": risk_id,
            "name": updated_name,
        }

        # Act: Update risk through the service
        updated_risk_domain = RiskService.update_risk(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the risk is updated
        assert updated_risk_domain.id == risk_id
        assert updated_risk_domain.name == updated_name

    def test_delete_risk_by_id_service(self, default_account):
        """Test deleting an risk by ID"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": risk_id,
        }

        # Act: Delete the risk
        RiskService.delete_risk_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted risk will fail
        with pytest.raises(ValueError):
            RiskService.get_risk_by_id(account_id=account_id, payload=delete_payload)

    def test_create_risk_service_owner_account_not_match(self, default_account):
        """Test creating an risk when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for risk creation
        payload = create_risk_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            RiskService.create_risk(account_id=account_id, payload=payload)

    def test_get_risk_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an risk when owner and account are not match"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": risk_id,
        }

        # Act: Retrieve the risk by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            RiskService.get_risk_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_risk_service_owner_account_not_match(self, default_account):
        """Test updating an risk when owner and account are not match"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Risk Service"

        updated_payload = {
            "id": risk_id,
            "name": updated_name,
        }

        # Act: Retrieve the risk by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            RiskService.update_risk(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_risk_service_owner_account_not_match(self, default_account):
        """Test deleting an risk when owner and account are not match"""

        # Arrange: Create an risk first
        account_id = default_account.id
        payload = create_risk_payload(account_id)
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": risk_id,
        }

        # Act: Retrieve the risk by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            RiskService.delete_risk_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_risk_by_id_service_with_not_existed_risk(self, default_account):
        """Test getting a not_existed risk"""

        # Arrange: Generate an risk id
        not_existed_risk_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_risk_id,
        }

        # Assert: Get risk with invalid id should fail
        with pytest.raises(ValueError):
            RiskService.get_risk_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_risk_service_with_not_existed_risk(self, default_account):
        """Test updating a not_existed risk"""

        # Arrange: Generate an risk id
        not_existed_risk_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Risk Service"

        updated_payload = {
            "id": not_existed_risk_id,
            "name": updated_name,
        }

        # Assert: Update risk with invalid id should fail
        with pytest.raises(ValueError):
            RiskService.update_risk(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_risk_service_with_not_existed_risk(self, default_account):
        """Test deleting a not_existed risk"""

        # Arrange: Generate an risk id
        not_existed_risk_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_risk_id,
        }

        # Assert: Delete risk with invalid id should fail
        with pytest.raises(ValueError):
            RiskService.delete_risk_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_risk_service_with_invalid_field(self, default_account):
        """Test creating an risk with invalid field using RiskService"""

        # Arrange: Given parameters for risk creation
        account_id = default_account.id
        payload = create_risk_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for risk creation
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)

        # Assert: The invalid field is not added
        assert hasattr(risk_domain, invalid_field_name) is False

    def test_update_risk_service_with_invalid_field(self, default_account):
        """Test updating an risk with invalid field using RiskService"""

        # Arrange: Given parameters for risk creation
        account_id = default_account.id
        payload = create_risk_payload(account_id)

        # Arrange: Given parameters for risk creation
        risk_domain = RiskService.create_risk(account_id=account_id, payload=payload)
        risk_id = risk_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Risk Service"

        updated_payload = {
            "id": risk_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the risk by ID
        updated_risk = RiskService.update_risk(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_risk, invalid_field_name) is False

    def test_create_risk_service_miss_required_field(self, default_account):
        """Test creating an risk using RiskService"""

        # Arrange: Given parameters for risk creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the RiskDomain
        payload = create_risk_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create risk when missing required field should raise ValueError
        with pytest.raises(ValueError):
            RiskService.create_risk(account_id=account_id, payload=payload)
