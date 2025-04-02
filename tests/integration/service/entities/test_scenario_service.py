from app.service.entities.scenario_service import ScenarioService
from tests.factory import create_account
from .factories import create_scenario_payload
from nanoid import generate
import pytest


class TestScenarioServiceCase:
    """Test cases for ScenarioService."""

    def test_create_scenario_service(self, default_account):
        """Test creating an scenario using ScenarioService"""

        # Arrange: Given parameters for scenario creation
        account_id = default_account.id

        # Define the expected fields that should be part of the ScenarioDomain
        payload = create_scenario_payload(account_id)
        fields = {
            "name",
            "description",
            "asset_allocation_percentage",
            "retire_age",
        }

        # Act: Call the service to create the scenario
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )

        # Assert: Ensure the returned ScenarioDomain matches the input payload
        for field in fields:
            # Make sure each field in ScenarioDomain matches the corresponding payload value
            assert (
                getattr(scenario_domain, field) == payload[field]
            ), f"Field {field} does not match expected value."
        assert (
            scenario_domain.owner.id == payload["owner_id"]
        ), "Field Owner ID does not match expected value."

        # Additional assertion: Check that the owner field in the domain matches the account_id
        assert (
            scenario_domain.owner.id == account_id
        ), "Owner ID does not match the provided account ID"

    def test_get_scenario_by_id_service(self, default_account):
        """Test retrieving an scenario by ID"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": scenario_id,
        }
        # Act: Retrieve the scenario by ID
        get_scenario_by_id_domain = ScenarioService.get_scenario_by_id(
            account_id=account_id,
            payload=get_payload,
        )

        assert get_scenario_by_id_domain.id == scenario_id
        assert get_scenario_by_id_domain == scenario_domain

    def test_get_scenarios_service(self, default_account):
        """Test retrieving a list of scenarios"""

        # Arrange: Get the initial count of scenarios
        account_id = default_account.id
        original_scenario_count = len(ScenarioService.get_scenarios(account_id))

        # Arrange: Create multiple scenarios
        new_scenario_count = 5
        created_scenarios = [
            ScenarioService.create_scenario(
                account_id, create_scenario_payload(account_id)
            )
            for _ in range(new_scenario_count)
        ]

        # Act: Retrieve updated list of scenarios
        scenarios_from_service = ScenarioService.get_scenarios(account_id)
        updated_scenario_count = len(scenarios_from_service)

        # Assert: Ensure each created scenario exists in the retrieved list
        assert all(exp in scenarios_from_service for exp in created_scenarios)

        # Assert: Ensure the total count has increased by the created number
        assert updated_scenario_count == original_scenario_count + new_scenario_count

    def test_update_scenario_service(self, default_account):
        """Test updating an scenario using ScenarioService"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Scenario Service"

        updated_payload = {
            "id": scenario_id,
            "name": updated_name,
        }

        # Act: Update scenario through the service
        updated_scenario_domain = ScenarioService.update_scenario(
            account_id=account_id, payload=updated_payload
        )

        # Assert: Ensure the scenario is updated
        assert updated_scenario_domain.id == scenario_id
        assert updated_scenario_domain.name == updated_name

    def test_delete_scenario_by_id_service(self, default_account):
        """Test deleting an scenario by ID"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define payload for deletion
        delete_payload = {
            "id": scenario_id,
        }

        # Act: Delete the scenario
        ScenarioService.delete_scenario_by_id(
            account_id=account_id,
            payload=delete_payload,
        )

        # Assert: Attempt to retrieve the deleted scenario will fail
        with pytest.raises(ValueError):
            ScenarioService.get_scenario_by_id(
                account_id=account_id, payload=delete_payload
            )

    def test_create_scenario_service_owner_account_not_match(self, default_account):
        """Test creating an scenario when owner and account are not match"""

        account_id = default_account.id

        # Arrange: Create a different account
        another_account_id = create_account().id

        # Arrange: Given parameters for scenario creation
        payload = create_scenario_payload(another_account_id)

        # Act: Given unmatch account_id and owner_id, it should raise Error

        with pytest.raises(PermissionError):
            ScenarioService.create_scenario(account_id=account_id, payload=payload)

    def test_get_scenario_by_id_service_owner_account_not_match(self, default_account):
        """Test getting an scenario when owner and account are not match"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": scenario_id,
        }

        # Act: Retrieve the scenario by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ScenarioService.get_scenario_by_id(
                account_id=another_account_id,
                payload=get_payload,
            )

    def test_update_scenario_service_owner_account_not_match(self, default_account):
        """Test updating an scenario when owner and account are not match"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Scenario Service"

        updated_payload = {
            "id": scenario_id,
            "name": updated_name,
        }

        # Act: Retrieve the scenario by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ScenarioService.update_scenario(
                account_id=another_account_id, payload=updated_payload
            )

    def test_delete_scenario_service_owner_account_not_match(self, default_account):
        """Test deleting an scenario when owner and account are not match"""

        # Arrange: Create an scenario first
        account_id = default_account.id
        payload = create_scenario_payload(account_id)
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": scenario_id,
        }

        # Act: Retrieve the scenario by ID with different account ID
        another_account_id = create_account().id

        with pytest.raises(PermissionError):
            ScenarioService.delete_scenario_by_id(
                account_id=another_account_id, payload=delete_payload
            )

    def test_get_scenario_by_id_service_with_not_existed_scenario(
        self, default_account
    ):
        """Test getting a not_existed scenario"""

        # Arrange: Generate an scenario id
        not_existed_scenario_id = generate(size=13)

        # Arrange: Define payload for retrieval
        get_payload = {
            "id": not_existed_scenario_id,
        }

        # Assert: Get scenario with invalid id should fail
        with pytest.raises(ValueError):
            ScenarioService.get_scenario_by_id(
                account_id=default_account.id,
                payload=get_payload,
            )

    def test_update_scenario_service_with_not_existed_scenario(self, default_account):
        """Test updating a not_existed scenario"""

        # Arrange: Generate an scenario id
        not_existed_scenario_id = generate(size=13)

        # Arrange: Define updated parameters
        updated_name = "Updated Scenario Service"

        updated_payload = {
            "id": not_existed_scenario_id,
            "name": updated_name,
        }

        # Assert: Update asset with invalid id should fail
        with pytest.raises(ValueError):
            ScenarioService.update_scenario(
                account_id=default_account.id, payload=updated_payload
            )

    def test_delete_scenario_service_with_not_existed_scenario(self, default_account):
        """Test deleting a not_existed scenario"""

        # Arrange: Generate an scenario id
        not_existed_scenario_id = generate(size=13)

        # Arrange: Define payload for retrieval
        delete_payload = {
            "id": not_existed_scenario_id,
        }

        # Assert: Delete asset with invalid id should fail
        with pytest.raises(ValueError):
            ScenarioService.delete_scenario_by_id(
                account_id=default_account.id, payload=delete_payload
            )

    def test_create_scenario_service_with_invalid_field(self, default_account):
        """Test creating an scenario with invalid field using ScenarioService"""

        # Arrange: Given parameters for scenario creation
        account_id = default_account.id
        payload = create_scenario_payload(account_id)

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        payload[invalid_field_name] = "this field is invalid"

        # Arrange: Given parameters for scenario creation
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )

        # Assert: The invalid field is not added
        assert hasattr(scenario_domain, invalid_field_name) is False

    def test_update_scenario_service_with_invalid_field(self, default_account):
        """Test updating an scenario with invalid field using ScenarioService"""

        # Arrange: Given parameters for scenario creation
        account_id = default_account.id
        payload = create_scenario_payload(account_id)

        # Arrange: Given parameters for scenario creation
        scenario_domain = ScenarioService.create_scenario(
            account_id=account_id, payload=payload
        )
        scenario_id = scenario_domain.id

        # Arrange: Define updated parameters
        updated_name = "Updated Scenario Service"

        updated_payload = {
            "id": scenario_id,
            "name": updated_name,
        }

        # Arrange: Add an invalid field
        invalid_field_name = "invalid_field"
        updated_payload[invalid_field_name] = "this field is invalid"

        # Act: Retrieve the scenario by ID
        updated_scenario = ScenarioService.update_scenario(
            account_id=account_id, payload=updated_payload
        )

        assert hasattr(updated_scenario, invalid_field_name) is False

    def test_create_scenario_service_miss_required_field(self, default_account):
        """Test creating an scenario using ScenarioService"""

        # Arrange: Given parameters for scenario creation
        account_id = default_account.id

        # Arrange: Define the expected fields that should be part of the ScenarioDomain
        payload = create_scenario_payload(account_id)

        # Arrange: Remove required field
        del payload["name"]

        # Assert: Create scenario when missing required field should raise ValueError
        with pytest.raises(ValueError):
            ScenarioService.create_scenario(account_id=account_id, payload=payload)
