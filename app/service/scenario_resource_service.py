from app.domain.associations import BaseAssociationDomain
from app.repository.entities import ScenarioRepo
from app.service.resource_mapper import ResourceFieldMapper
from app.domain.entities import ScenarioDomain, ResourceDomain


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
    def _get_scenario_domain(account_id: str, payload: dict) -> ScenarioDomain:
        # Get scenario id
        scenario_id = payload.get("scenario_id")
        if not scenario_id:
            raise ValueError("Scenario ID is required")

        # Get scenario domain by ScenarioRepo
        scenario_from_repo = ScenarioRepo.get_by_id(scenario_id)
        if not scenario_from_repo:
            raise ValueError(f"Scenario with ID {scenario_id} not found")

        # Check if the user own the resource
        ScenarioResourceService._check_ownership(scenario_from_repo, account_id)
        return scenario_from_repo

    @staticmethod
    def _get_resource_id(resource_type: str, payload: dict) -> str:
        resource_id = payload[f"{resource_type}_id"]
        if not resource_id:
            raise ValueError(f"{resource_type.capitalize} ID is required")
        return resource_id

    @staticmethod
    def _get_resource_domain(
        account_id: str, mapper: ResourceFieldMapper, payload: dict
    ) -> ResourceDomain:
        # Get scenario id
        resource_type = mapper.resource_type
        resource_id = ScenarioResourceService._get_resource_id(resource_type, payload)

        # Get scenario domain by ScenarioRepo
        resource_repo = mapper.resource_repo_cls
        resource_domain_from_repo = resource_repo.get_by_id(resource_id)

        # Check if resource existed
        if not resource_domain_from_repo:
            raise ValueError(
                f"{resource_type.capitalize} with ID {resource_id} not found"
            )

        # Check if the user own the resource
        ScenarioResourceService._check_ownership(resource_domain_from_repo, account_id)
        return resource_domain_from_repo

    @staticmethod
    def _check_ownership(resource_domain: ResourceDomain, account_id: str) -> str:
        # Check if the account owns the scenario
        owner = (
            resource_domain.parent
            if hasattr(resource_domain, "parent")
            else resource_domain.owner
        )

        if owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this resource")

        return f"Account {account_id} own this resource"

    @staticmethod
    def _generate_assoc_payload(mapper: ResourceFieldMapper, payload: dict) -> dict:
        # Check if required fields provided
        ScenarioResourceService._check_required_fields_provided(
            mapper.cid_fields, payload
        )

        # Filter payload to only include allowed fields
        return {
            field: payload[field]
            for field in mapper.association_fields
            if field in payload
        }

    @staticmethod
    def _check_required_fields_provided(cid_fields: set, payload: dict) -> str:
        # Validate required fields
        missing_fields = cid_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        else:
            return "Required fields are provided in the payload."

    @staticmethod
    def add_resource_by_id(
        account_id: str, resource_type: str, payload: dict
    ) -> BaseAssociationDomain:
        """Add resource to given scenario with validated owner."""

        # Get scenario domain
        scenario_domain = ScenarioResourceService._get_scenario_domain(
            account_id=account_id, payload=payload
        )

        # Create resource mapper
        mapper = ResourceFieldMapper.by_resource_type(resource_type)

        # Get resource domain
        resource_domain = ScenarioResourceService._get_resource_domain(
            account_id=account_id, mapper=mapper, payload=payload
        )

        # Generate assoc payload
        assoc_payload = ScenarioResourceService._generate_assoc_payload(
            mapper=mapper, payload=payload
        )

        return ScenarioRepo.add_resource(
            scenario=scenario_domain, resource=resource_domain, **assoc_payload
        )

    @staticmethod
    def get_resource_by_id(
        account_id: str, resource_type: str, payload: dict
    ) -> BaseAssociationDomain:
        # Get scenario domain
        scenario_domain = ScenarioResourceService._get_scenario_domain(
            account_id, payload
        )

        # Create resource mapper
        mapper = ResourceFieldMapper.by_resource_type(resource_type)

        # Get resource domain
        resource_domain = ScenarioResourceService._get_resource_domain(
            account_id=account_id, mapper=mapper, payload=payload
        )

        return ScenarioRepo.get_resource_by_id(
            scenario=scenario_domain,
            resource_type=mapper.resource_domain_cls,
            resource_id=resource_domain.id,
        )

    @staticmethod
    def get_resource_list(account_id: str) -> list[BaseAssociationDomain]:
        pass
        # """Retrieve all scenarios for a given account."""
        # return ScenarioRepo.get_list(account_id)

    @staticmethod
    def get_all_resource(account_id: str) -> dict[list[BaseAssociationDomain]]:
        pass
        # """Retrieve all scenarios for a given account."""
        # return ScenarioRepo.get_list(account_id)

    @staticmethod
    def update_resource_by_id(
        account_id: str, resource_type: str, payload: dict
    ) -> BaseAssociationDomain:
        # Get scenario domain
        scenario_domain = ScenarioResourceService._get_scenario_domain(
            account_id=account_id, payload=payload
        )
        # Create resource mapper
        mapper = ResourceFieldMapper.by_resource_type(resource_type)

        # Get resource domain
        resource_domain = ScenarioResourceService._get_resource_domain(
            account_id=account_id, mapper=mapper, payload=payload
        )

        # Generate assoc payload
        assoc_payload = ScenarioResourceService._generate_assoc_payload(
            mapper=mapper, payload=payload
        )
        return ScenarioRepo.update_resource(
            scenario=scenario_domain,
            resource=resource_domain,
            **assoc_payload,
        )

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
