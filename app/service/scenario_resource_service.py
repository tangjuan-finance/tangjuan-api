from app.domain.entities import ResourceDomain
from app.repository.entities import ScenarioRepo
from app.service.resource_mapper import ResourceFieldMapper


class ScenarioResourceService:
    _required_fields = {
        "name",
        "asset_allocation_percentage",
        "retire_age",
    }
    _all_fields = _required_fields | {
        "description",
    }

    @staticmethod
    def add_resource_by_id(
        account_id: str, resource_type: str, payload: dict
    ) -> ResourceDomain:
        """Create a new scenario with validated owner."""

        # Create resource mapper
        mapper = ResourceFieldMapper.by_resource_type(resource_type)

        # Get scenario domain
        scenario_id = payload["scenario_id"]
        scenario_domain = ScenarioRepo.get_by_id(scenario_id)

        # Get resource domain
        resource_id = payload[f"{resource_type}_id"]
        domain_repo = mapper.resource_repo_cls
        resource_domain = domain_repo(resource_id)

        # Check if both the scenario and the resource is owned by given account
        if scenario_domain.owner.id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to access this scenario"
            )

        if resource_domain.owner.id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to access this resource"
            )

        # Use mapper to get required fields and all fields
        required_fields = mapper.required_fields
        all_fields = mapper.all_fields

        # Validate required fields
        missing_fields = required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Filter payload to only include allowed fields
        assoc_payload = {
            field: payload[field] for field in all_fields if field in payload
        }

        return ScenarioRepo.add_resource(
            scenario=scenario_domain, resource=resource_domain, **assoc_payload
        )

    @staticmethod
    def get_resource_by_id(account_id: str, payload: dict) -> ResourceDomain:
        pass
        # """Retrieve a specific scenario by ID."""
        # scenario_id = payload.get("id")
        # if not scenario_id:
        #     raise ValueError("Scenario ID is required")
        # scenario_from_repo = ScenarioRepo.get_by_id(scenario_id)

        # if not scenario_from_repo:
        #     raise ValueError(f"Scenario with ID {scenario_id} not found")

        # # Check if the account owns the scenario
        # if scenario_from_repo.owner.id != account_id:
        #     raise PermissionError(f"Account {account_id} does not own this resource")

        # return scenario_from_repo

    @staticmethod
    def get_resource_list(account_id: str) -> list[ResourceDomain]:
        pass
        # """Retrieve all scenarios for a given account."""
        # return ScenarioRepo.get_list(account_id)

    @staticmethod
    def get_all_resource(account_id: str) -> dict[list[ResourceDomain]]:
        pass
        # """Retrieve all scenarios for a given account."""
        # return ScenarioRepo.get_list(account_id)

    @staticmethod
    def update_resource_by_id(account_id: str, payload: dict) -> ResourceDomain:
        pass
        # """Update an scenario by ID if it exists."""
        # scenario_from_repo = ScenarioResourceService.get_scenario_by_id(account_id, payload)

        # for field in ScenarioResourceService._all_fields:
        #     if field in payload:
        #         setattr(scenario_from_repo, field, payload[field])

        # return ScenarioRepo.save(scenario_from_repo)

    @staticmethod
    def remove_resource_by_id(account_id: str, payload: dict) -> str:
        pass
        # """Delete an scenario by ID if it exists."""
        # scenario = ScenarioResourceService.get_scenario_by_id(
        #     account_id, payload
        # )  # Raises if not found or unauthorized
        # ScenarioRepo.delete_by_id(scenario.id)
        # return f"Scenario {scenario.id} deleted successfully"
