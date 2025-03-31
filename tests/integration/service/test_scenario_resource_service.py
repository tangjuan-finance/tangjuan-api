from app.service.scenario_resource_service import ScenarioResourceService
from app.domain.entities import AccountDomain
from types import MappingProxyType
from tests.integration.service.factories import (
    # create_account,
    # create_scenario,
    create_scenario_child_payload,
    create_scenario_asset_payload,
    create_scenario_expense_payload,
    create_scenario_house_payload,
    create_scenario_income_payload,
    create_scenario_liability_payload,
    create_scenario_risk_payload,
)

# from nanoid import generate
import pytest
from tests.resource_mapper import ResourceTestMapper
from app.service.resource_mapper import ResourceFieldMapper


class TestScenarioResourceServiceCase:
    """Test cases for ScenarioResourceService."""

    _RESOURCE_PAYLOAD_MAPPING = MappingProxyType(
        {
            "child": create_scenario_child_payload,
            "liability": create_scenario_liability_payload,
            "expense": create_scenario_expense_payload,
            "income": create_scenario_income_payload,
            "house": create_scenario_house_payload,
            "risk": create_scenario_risk_payload,
            "asset": create_scenario_asset_payload,
        }
    )

    resource_param = {
        "param": "resource_type",
        "payload": [
            ("expense"),
            ("income"),
            ("house"),
            ("child"),
            ("risk"),
            ("asset"),
            ("liability"),
        ],
    }

    def _create_resource(owner: AccountDomain, resource_type: str) -> str:
        mapper = ResourceTestMapper.by_resource_type(resource_type)
        if mapper.resource_type == "child":
            resource_domain = mapper.resource_domain_factory(parent=owner)
        else:
            resource_domain = mapper.resource_domain_factory(owner=owner)
        resource_repo = mapper.resource_repo_cls
        resource_domain_from_repo = resource_repo.create(resource_domain)
        return resource_domain_from_repo.id

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_by_scenario_resource_service(
        self, default_account, default_scenario, resource_type
    ):
        """Test creating a scenario using ScenarioService"""

        # Arrange: Given parameters for scenario creation
        account_id = default_account.id
        scenario_id = default_scenario.id

        # Arrange: Create a resource based on the resource_type
        resource_id = TestScenarioResourceServiceCase._create_resource(
            default_account, resource_type
        )

        # Arrange: Define the expected fields that should be part of the ScenarioResourceDomain
        create_resource_payload_func = (
            TestScenarioResourceServiceCase._RESOURCE_PAYLOAD_MAPPING[resource_type]
        )
        payload = create_resource_payload_func(
            scenario_id=scenario_id, **{f"{resource_type}_id": resource_id}
        )

        # Act: Call the service to create the scenario
        scenario_resource_assoc = ScenarioResourceService.add_resource_by_id(
            account_id=account_id, resource_type=resource_type, payload=payload
        )

        # Assert: Ensure the returned ScenarioDomain matches the input payload
        association_fields = ResourceFieldMapper.by_resource_type(
            resource_type
        ).association_fields
        for field in association_fields:
            # Make sure each field in ScenarioDomain matches the corresponding payload value
            assert (
                getattr(scenario_resource_assoc, field) == payload[field]
            ), f"Field {field} does not match expected value."
