from app.domain.entities import ScenarioDomain
from app.repository.entities import ScenarioRepo
from .mixin import OwnerRequiredServiceMixin


class ScenarioService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "asset_allocation_percentage",
        "retire_age",
    }
    _all_fields = _required_fields | {
        "description",
    }

    @staticmethod
    def create_scenario(account_id: str, payload: dict) -> ScenarioDomain:
        """Create a new scenario with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create scenario under the given owner"
            )

        # Validate required fields
        missing_fields = ScenarioService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = ScenarioService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        scenario_payload = {
            field: payload[field]
            for field in ScenarioService._all_fields
            if field in payload
        }
        scenario_payload["owner"] = owner

        # Create the scenario
        scenario = ScenarioDomain(**scenario_payload)
        return ScenarioRepo.create(scenario)

    @classmethod
    def get_scenario_by_id(cls, account_id: str, payload: dict) -> ScenarioDomain:
        """Retrieve a specific scenario by ID."""
        scenario_id = payload.get("id")
        if not scenario_id:
            raise ValueError("Scenario ID is required")
        scenario_from_repo = ScenarioRepo.get_by_id(scenario_id)

        if not scenario_from_repo:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        # Check if the account owns the scenario
        cls._check_entity_ownership_by_id(
            account_id=account_id, owner_id=scenario_from_repo.owner.id
        )

        return scenario_from_repo

    @staticmethod
    def get_scenarios(account_id: str) -> list[ScenarioDomain]:
        """Retrieve all scenarios for a given account."""
        return ScenarioRepo.get_list(account_id)

    @staticmethod
    def update_scenario(account_id: str, payload: dict) -> ScenarioDomain:
        """Update an scenario by ID if it exists."""
        scenario_from_repo = ScenarioService.get_scenario_by_id(account_id, payload)

        for field in ScenarioService._all_fields:
            if field in payload:
                setattr(scenario_from_repo, field, payload[field])

        return ScenarioRepo.save(scenario_from_repo)

    @staticmethod
    def delete_scenario_by_id(account_id: str, payload: dict) -> str:
        """Delete an scenario by ID if it exists."""
        scenario = ScenarioService.get_scenario_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        ScenarioRepo.delete_by_id(scenario.id)
        return f"Scenario {scenario.id} deleted successfully"
