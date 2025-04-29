from app.service.entities.child_saving_plan_service import ChildSavingPlanService
from tests.factory import create_account
from .factories import create_child_saving_plan_payload
from nanoid import generate
import pytest


class TestChildSavingPlanServiceCase:
    """Test cases for ChildSavingPlanService."""

    def test_create_child_saving_plan_service(self, default_account):
        """Test creating an child_saving_plan using ChildSavingPlanService"""

        # Arrange: Given parameters for child_saving_plan creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ChildSavingPlanDomain
        payload = create_child_saving_plan_payload(account_id)
        fields = {
            "name",
            "description",
            "independent_age",
        }

        # Act: Call the service to create the child_saving_plan
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned ChildSavingPlanDomain matches the input payload
        for field in fields:
            # Make sure each field in ChildSavingPlanDomain matches the corresponding payload value
            assert (
                getattr(child_saving_plan_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            child_saving_plan_domain.owner_id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            child_saving_plan_domain.owner_id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_child_saving_plan_by_id_service(self, default_account):
        """Test retrieving an child_saving_plan by ID"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": child_saving_plan_id,
        }
        # Act: Retrieve the child_saving_plan by ID
        get_child_saving_plan_by_id_domain = (
            ChildSavingPlanService.get_child_saving_plan_by_id(
                account_id=account_id,
                payload=get_payload,
            )
        )

        assert get_child_saving_plan_by_id_domain.id == child_saving_plan_id
        assert get_child_saving_plan_by_id_domain == child_saving_plan_domain

    def test_get_child_saving_plans_service(self, default_account):
        """Test retrieving a list of child_saving_plans"""

        # Arrange: Get the initial count of child_saving_plans
        account_id = default_account.id
        original_child_saving_plan_count = len(
            ChildSavingPlanService.get_child_saving_plans(account_id)
        )

        # Arrange: Create multiple child_saving_plans
        new_child_saving_plan_count = 5
        created_child_saving_plans = [
            ChildSavingPlanService.create_child_saving_plan(
                account_id, create_child_saving_plan_payload(account_id)
            )
            for _ in range(new_child_saving_plan_count)
        ]

        # Act: Retrieve updated list of child_saving_plans
        child_saving_plans_from_service = ChildSavingPlanService.get_child_saving_plans(
            account_id
        )
        updated_child_saving_plan_count = len(child_saving_plans_from_service)

        # Assert: Ensure each created child_saving_plan exists in the retrieved list
        assert all(
            exp in child_saving_plans_from_service for exp in created_child_saving_plans
        )

        # Assert: Ensure the total count has increased by the created number
        assert (
            updated_child_saving_plan_count
            == original_child_saving_plan_count + new_child_saving_plan_count
        )

    def test_update_child_saving_plan_service(self, default_account):
        """Test updating an child_saving_plan using ChildSavingPlanService"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "id": child_saving_plan_id,
            "name": updated_name,
        }

        # Act: Update child_saving_plan through the service
        updated_child_saving_plan_domain = (
            ChildSavingPlanService.update_child_saving_plan(
                account_id=account_id, payload=updated_payload
            )
        )

        # Assert: Ensure the child_saving_plan is updated
        assert updated_child_saving_plan_domain.id == child_saving_plan_id
        assert updated_child_saving_plan_domain.name == updated_name

    def test_delete_child_saving_plan_by_id_service(self, default_account):
        """Test deleting an child_saving_plan by ID"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": child_saving_plan_id,
        }

        # Act: Delete the child_saving_plan
        ChildSavingPlanService.delete_child_saving_plan_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted child_saving_plan will fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.get_child_saving_plan_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_child_saving_plan_service_owner_account_not_match(
        self, default_account
    ):
        """Test creating an child_saving_plan when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for child_saving_plan creation
        payload = create_child_saving_plan_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            ChildSavingPlanService.create_child_saving_plan(
                account_id=account_id, payload=payload
            )

    def test_get_child_saving_plan_by_id_service_owner_account_not_match(
        self, default_account
    ):
        """Test getting an child_saving_plan when owner and account are not match"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": child_saving_plan_id,
        }

        # Act: Retrieve the child_saving_plan by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.get_child_saving_plan_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_child_saving_plan_service_owner_account_not_match(
        self, default_account
    ):
        """Test updating an child_saving_plan when owner and account are not match"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "id": child_saving_plan_id,
            "name": updated_name,
        }

        # Act: Retrieve the child_saving_plan by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.update_child_saving_plan(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_child_saving_plan_service_owner_account_not_match(
        self, default_account
    ):
        """Test deleting an child_saving_plan when owner and account are not match"""

        # Arrange: Create an child_saving_plan first
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": child_saving_plan_id,
        }

        # Act: Retrieve the child_saving_plan by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.delete_child_saving_plan_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_child_saving_plan_by_id_service_with_not_existed_child_saving_plan(
        self, default_account
    ):
        """Test getting a not_existed child_saving_plan"""

        # Arrange: Generate an child_saving_plan id
        not_existed_child_saving_plan_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_child_saving_plan_id,
        }

        # Assert: Get child_saving_plan with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.get_child_saving_plan_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_child_saving_plan_service_with_not_existed_child_saving_plan(
        self, default_account
    ):
        """Test updating a not_existed child_saving_plan"""

        # Arrange: Generate an child_saving_plan id
        not_existed_child_saving_plan_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "id": not_existed_child_saving_plan_id,
            "name": updated_name,
        }

        # Assert: Update child_saving_plan with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.update_child_saving_plan(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_child_saving_plan_service_with_not_existed_child_saving_plan(
        self, default_account
    ):
        """Test deleting a not_existed child_saving_plan"""

        # Arrange: Generate an child_saving_plan id
        not_existed_child_saving_plan_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_child_saving_plan_id,
        }

        # Assert: Delete child_saving_plan with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.delete_child_saving_plan_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_child_saving_plan_service_with_invalid_field(self, default_account):
        """Test creating an child_saving_plan with invalid field using ChildSavingPlanService"""

        # Arrange: Given parameters for child_saving_plan creation
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for child_saving_plan creation
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(child_saving_plan_domain, invalid_field_name) is False

    def test_update_child_saving_plan_service_with_invalid_field(self, default_account):
        """Test updating an child_saving_plan with invalid field using ChildSavingPlanService"""

        # Arrange: Given parameters for child_saving_plan creation
        account_id = default_account.id
        payload = create_child_saving_plan_payload(account_id)

        # Arrange: Given parameters for child_saving_plan creation
        child_saving_plan_domain = ChildSavingPlanService.create_child_saving_plan(
            account_id=account_id, payload=payload
        )
        child_saving_plan_id = child_saving_plan_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "id": child_saving_plan_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the child_saving_plan by ID
        updated_child_saving_plan = ChildSavingPlanService.update_child_saving_plan(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_child_saving_plan, invalid_field_name) is False

    def test_create_child_saving_plan_service_miss_required_field(
        self, default_account
    ):
        """Test creating an child_saving_plan using ChildSavingPlanService"""

        # Arrange: Given parameters for child_saving_plan creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ChildSavingPlanDomain
        payload = create_child_saving_plan_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create child_saving_plan when missing required field should raise ValueError
        with pytest.raises(ValueError):
            ChildSavingPlanService.create_child_saving_plan(
                account_id=account_id, payload=payload
            )
