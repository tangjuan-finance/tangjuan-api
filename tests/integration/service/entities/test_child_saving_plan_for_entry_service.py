from app.service.entities.child_saving_plan_service import ChildSavingPlanService
from app.domain.entities import ChildSavingAmountEntryDomain
from tests.factory import create_account
from .factories import create_child_saving_amount_entry_payload
from nanoid import generate
import pytest


class TestChildSavingPlanServiceForEntryCase:
    """Test cases for ChildSavingPlanService."""

    def _create_entry(
        self, account_id: str, plan_id: str
    ) -> ChildSavingAmountEntryDomain:
        payload = create_child_saving_amount_entry_payload(plan_id)
        return ChildSavingPlanService.add_amount_entry(
            account_id=account_id, plan_id=plan_id, payload=payload
        )

    def test_create_child_saving_amount_entry_service(
        self, default_account, default_child_saving_plan
    ):
        """Test creating an child_saving_amount_entry using ChildSavingPlanService"""

        # Arrange: Given parameters for child_saving_amount_entry creation
        account_id = default_account.id
        plan_id = default_child_saving_plan.id

        # Arrange: Define the expected fields that should be part of the ChildSavingAmountEntryDomain
        payload = create_child_saving_amount_entry_payload(plan_id)
        fields = {
            "name",
            "description",
            "amount",
            "start_age",
            "end_age",
        }

        # Act: Call the service to create the child_saving_amount_entry
        entry = ChildSavingPlanService.add_amount_entry(
            account_id=account_id, plan_id=plan_id, payload=payload
        )

        # Assert: Ensure the returned ChildSavingAmountEntryDomain matches the input payload
        for field in fields:
            # Make sure each field in ChildSavingAmountEntryDomain matches the corresponding payload value
            assert (
                getattr(entry, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            entry.child_saving_plan_id == payload["child_saving_plan_id"]
        ), "Field Plan ID does not match expected value."

    def test_get_child_saving_amount_entry_by_id_service(
        self, default_account, default_child_saving_plan
    ):
        """Test retrieving an child_saving_amount_entry by ID"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id

        entry = self._create_entry(account_id, plan_id)
        entry_id = entry.id

        # Act: Retrieve the amount_entry by ID
        get_entry = ChildSavingPlanService.get_amount_entry_by_id(
            account_id=account_id,
            plan_id=plan_id,
            entry_id=entry_id,
        )

        assert get_entry.id == entry_id
        assert get_entry == entry

    def test_get_amount_entries_service(
        self, default_account, default_child_saving_plan
    ):
        """Test retrieving a list of amount_entries"""

        # Arrange: Get the initial count of amount_entries
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        original_child_saving_amount_entry_count = len(
            ChildSavingPlanService.list_amount_entries(account_id, plan_id)
        )

        # Arrange: Create multiple amount_entries
        new_child_saving_amount_entry_count = 5
        created_amount_entries = [
            ChildSavingPlanService.add_amount_entry(
                account_id,
                plan_id,
                create_child_saving_amount_entry_payload(plan_id),
            )
            for _ in range(new_child_saving_amount_entry_count)
        ]

        # Act: Retrieve updated list of amount_entries
        amount_entries_from_service = ChildSavingPlanService.list_amount_entries(
            account_id, plan_id
        )
        updated_child_saving_amount_entry_count = len(amount_entries_from_service)

        # Assert: Ensure each created amount_entry exists in the retrieved list
        assert all(exp in amount_entries_from_service for exp in created_amount_entries)

        # Assert: Ensure the total count has increased by the created number
        assert (
            updated_child_saving_amount_entry_count
            == original_child_saving_amount_entry_count
            + new_child_saving_amount_entry_count
        )

    def test_update_child_saving_amount_entry_service(
        self, default_account, default_child_saving_plan
    ):
        """Test updating an amount_entry using ChildSavingPlanService"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)
        entry_id = entry.id

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "name": updated_name,
        }

        # Act: Update amount_entry through the service
        updated_child_saving_amount_entry_domain = (
            ChildSavingPlanService.update_amount_entry_by_id(
                account_id=account_id,
                plan_id=plan_id,
                entry_id=entry_id,
                payload=updated_payload,
            )
        )

        # Assert: Ensure the amount_entry is updated
        assert updated_child_saving_amount_entry_domain.id == entry_id
        assert updated_child_saving_amount_entry_domain.name == updated_name

    def test_delete_child_saving_amount_entry_by_id_service(
        self, default_account, default_child_saving_plan
    ):
        """Test deleting an amount_entry by ID"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)
        entry_id = entry.id

        # Act: Delete the amount_entry
        ChildSavingPlanService.remove_amount_entry_by_id(
            account_id=account_id,
            plan_id=plan_id,
            entry_id=entry_id,
        )

        # Assert: Attempt to retrieve the deleted amount_entry will fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.get_amount_entry_by_id(
                account_id=account_id,
                plan_id=plan_id,
                entry_id=entry_id,
            )

    # === SAD test below ===

    def test_create_child_saving_amount_entry_service_owner_account_not_match(
        self, default_child_saving_plan
    ):
        """Test creating an amount_entry when owner and account are not match"""

        # Arrange: Given parameters for amount_entry creation
        plan_id = default_child_saving_plan.id
        payload = create_child_saving_amount_entry_payload(plan_id)

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Act: Given unmatch account_id and owner_id, it should raise Error
        with pytest.raises(PermissionError):
            ChildSavingPlanService.add_amount_entry(
                another_account_id, plan_id, payload
            )

    def test_get_child_saving_amount_entry_by_id_service_owner_account_not_match(
        self, default_account, default_child_saving_plan
    ):
        """Test getting an amount_entry when owner and account are not match"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)

        # Act: Retrieve the amount_entry by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.get_amount_entry_by_id(
                another_account_id, plan_id, entry.id
            )

    def test_update_child_saving_amount_entry_service_owner_account_not_match(
        self, default_account, default_child_saving_plan
    ):
        """Test updating an amount_entry when owner and account are not match"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "name": updated_name,
        }

        # Act: Retrieve the amount_entry by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.update_amount_entry_by_id(
                another_account_id, plan_id, entry.id, payload=updated_payload
            )

    def test_delete_child_saving_amount_entry_service_owner_account_not_match(
        self, default_account, default_child_saving_plan
    ):
        """Test deleting an amount_entry when owner and account are not match"""

        # Arrange: Create an amount_entry first
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)

        # Act: Retrieve the amount_entry by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ChildSavingPlanService.remove_amount_entry_by_id(
                another_account_id, plan_id, entry.id
            )

    def test_get_child_saving_amount_entry_by_id_service_with_not_existed_amount_entry(
        self, default_account, default_child_saving_plan
    ):
        """Test getting a not_existed amount_entry"""

        # Arrange: Generate an amount_entry id
        fake_id = generate(size=13)

        # Assert: Get amount_entry with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.get_amount_entry_by_id(
                default_account.id, default_child_saving_plan.id, fake_id
            )

    def test_update_child_saving_amount_entry_service_with_not_existed_amount_entry(
        self, default_account, default_child_saving_plan
    ):
        """Test updating a not_existed amount_entry"""

        # Arrange: Generate an amount_entry id
        fake_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "name": updated_name,
        }

        # Assert: Update amount_entry with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.update_amount_entry_by_id(
                default_account.id,
                default_child_saving_plan.id,
                fake_id,
                updated_payload,
            )

    def test_delete_child_saving_amount_entry_service_with_not_existed_amount_entry(
        self, default_account, default_child_saving_plan
    ):
        """Test deleting a not_existed amount_entry"""

        # Arrange: Generate an amount_entry id
        fake_id = generate(size=13)

        # Assert: Delete amount_entry with invalid id should fail
        with pytest.raises(ValueError):
            ChildSavingPlanService.remove_amount_entry_by_id(
                default_account.id, default_child_saving_plan.id, fake_id
            )

    def test_create_child_saving_amount_entry_service_with_invalid_field(
        self, default_account, default_child_saving_plan
    ):
        """Test creating an amount_entry with invalid field using ChildSavingPlanService"""

        # Arrange: Given parameters for amount_entry creation
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        payload = create_child_saving_amount_entry_payload(plan_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for amount_entry creation
        amount_entry_domain = ChildSavingPlanService.add_amount_entry(
            account_id, plan_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(amount_entry_domain, invalid_field_name) is False

    def test_update_child_saving_amount_entry_service_with_invalid_field(
        self, default_account, default_child_saving_plan
    ):
        """Test updating an amount_entry with invalid field using ChildSavingPlanService"""

        # Arrange: Given parameters for amount_entry creation
        account_id = default_account.id
        plan_id = default_child_saving_plan.id
        entry = self._create_entry(account_id, plan_id)

        # Arrange: Define updated parameters
        updated_name = "Updated ChildSavingPlan Service"

        updated_payload = {
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the amount_entry by ID
        updated_amount_entry = ChildSavingPlanService.update_amount_entry_by_id(
            account_id, plan_id, entry.id, updated_payload
        )

        assert hasattr(updated_amount_entry, invalid_field_name) is False

    def test_create_child_saving_amount_entry_service_miss_required_field(
        self, default_account, default_child_saving_plan
    ):
        """Test creating an amount_entry using ChildSavingPlanService"""

        # Arrange: Given parameters for amount_entry creation
        account_id = default_account.id
        plan_id = default_child_saving_plan.id

        # Arrange: Define the expected fields that should be part of the ChildSavingAmountEntryDomain
        payload = create_child_saving_amount_entry_payload(plan_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create amount_entry when missing required field should raise ValueError
        with pytest.raises(ValueError):
            ChildSavingPlanService.add_amount_entry(
                account_id, plan_id, payload=payload
            )
