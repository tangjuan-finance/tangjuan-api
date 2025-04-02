# from app.service.scenario_resource_service import ScenarioResourceService
# from app.domain.associations import BaseAssociationDomain
# from app.domain.entities import AccountDomain
# from types import MappingProxyType
# from tests.integration.service.factories import (
#     # create_account,
#     # create_scenario,
#     create_scenario_child_payload,
#     create_scenario_asset_payload,
#     create_scenario_expense_payload,
#     create_scenario_house_payload,
#     create_scenario_income_payload,
#     create_scenario_liability_payload,
#     create_scenario_risk_payload,
# )

# # from nanoid import generate
# import pytest
# from tests.resource_mapper import ResourceTestMapper
# from app.service.resource_mapper import ResourceFieldMapper


# class TestScenarioResourceServiceCase:
#     """Test cases for ScenarioResourceService."""

#     _RESOURCE_PAYLOAD_MAPPING = MappingProxyType(
#         {
#             "child": create_scenario_child_payload,
#             "liability": create_scenario_liability_payload,
#             "expense": create_scenario_expense_payload,
#             "income": create_scenario_income_payload,
#             "house": create_scenario_house_payload,
#             "risk": create_scenario_risk_payload,
#             "asset": create_scenario_asset_payload,
#         }
#     )

#     resource_param = {
#         "param": "resource_type",
#         "payload": [
#             ("expense"),
#             ("income"),
#             ("house"),
#             ("child"),
#             ("risk"),
#             ("asset"),
#             ("liability"),
#         ],
#     }

#     @staticmethod
#     def _create_resource(owner: AccountDomain, resource_type: str) -> str:
#         mapper = ResourceTestMapper.by_resource_type(resource_type)
#         if mapper.resource_type == "child":
#             resource_domain = mapper.resource_domain_factory(parent=owner)
#         else:
#             resource_domain = mapper.resource_domain_factory(owner=owner)
#         resource_repo = mapper.resource_repo_cls
#         resource_domain_from_repo = resource_repo.create(resource_domain)
#         return resource_domain_from_repo.id

#     @staticmethod
#     def _add_resource_to_scenario(
#         account_id: str, scenario_id: str, resource_id: str, resource_type: str
#     ) -> BaseAssociationDomain:
#         # Arrange: Define the expected fields that should be part of the ScenarioResourceDomain
#         create_resource_payload_func = (
#             TestScenarioResourceServiceCase._RESOURCE_PAYLOAD_MAPPING[resource_type]
#         )
#         payload = create_resource_payload_func(
#             scenario_id=scenario_id, **{f"{resource_type}_id": resource_id}
#         )

#         # Act: Call the service to create the scenario
#         return ScenarioResourceService.add_resource_by_id(
#             account_id=account_id, resource_type=resource_type, payload=payload
#         )

#     @staticmethod
#     def _assert_assoc_fields_with_payload(assoc: BaseAssociationDomain, payload: dict):
#         # Assert: Ensure the returned ScenarioDomain matches the input payload
#         association_fields = ResourceFieldMapper.from_assoc(assoc).association_fields
#         for field in association_fields:
#             # Make sure each field in ScenarioDomain matches the corresponding payload value
#             assert (
#                 getattr(assoc, field) == payload[field]
#             ), f"Field {field} does not match expected value."

#     @staticmethod
#     def _assert_assoc_fields_with_another_assoc(
#         assoc: BaseAssociationDomain, another_assoc: BaseAssociationDomain
#     ):
#         # Assert: Ensure the returned ScenarioDomain matches the input payload
#         association_fields = ResourceFieldMapper.from_assoc(assoc).association_fields
#         for field in association_fields:
#             # Make sure each field in ScenarioDomain matches the corresponding payload value
#             assert getattr(assoc, field) == getattr(
#                 another_assoc, field
#             ), f"Field {field} does not match expected value."

#     @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
#     def test_add_resource_through_scenario_resource_service(
#         self, default_account, default_scenario, resource_type
#     ):
#         """Test adding a resource to given scenario with given account using ScenarioResourceService"""

#         # Arrange: Getting account and scenario id
#         account_id, scenario_id = default_account.id, default_scenario.id

#         # Arrange: Create a resource based on the resource_type
#         resource_id = TestScenarioResourceServiceCase._create_resource(
#             default_account, resource_type
#         )

#         # Arrange: Define the expected fields that should be part of the ScenarioResourceDomain
#         create_resource_payload_func = (
#             TestScenarioResourceServiceCase._RESOURCE_PAYLOAD_MAPPING[resource_type]
#         )
#         payload = create_resource_payload_func(
#             scenario_id=scenario_id, **{f"{resource_type}_id": resource_id}
#         )

#         # Act: Call the service to create the scenario
#         scenario_resource_assoc = ScenarioResourceService.add_resource_by_id(
#             account_id=account_id, resource_type=resource_type, payload=payload
#         )

#         # Assert: Ensure the returned ScenarioDomain matches the input payload
#         TestScenarioResourceServiceCase._assert_assoc_fields_with_payload(
#             assoc=scenario_resource_assoc, payload=payload
#         )

#     @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
#     def test_get_resource_by_id_through_scenario_resource_service(
#         self, default_account, default_scenario, resource_type
#     ):
#         """Test getting a resource to given scenario with given account using ScenarioResourceService"""

#         # Arrange: Getting account and scenario id
#         account_id, scenario_id = default_account.id, default_scenario.id

#         # Arrange: Create a resource based on the resource_type
#         resource_id = TestScenarioResourceServiceCase._create_resource(
#             default_account, resource_type
#         )

#         # Arrange: Add resource to given scenario by given account
#         origin_assoc = TestScenarioResourceServiceCase._add_resource_to_scenario(
#             account_id=account_id,
#             scenario_id=scenario_id,
#             resource_id=resource_id,
#             resource_type=resource_type,
#         )

#         # Arrange: Set the get payload with scenario ID and resource ID
#         get_payload = {
#             "scenario_id": scenario_id,
#             **{f"{resource_type}_id": resource_id},
#         }

#         # Act: Update the resource by ScenarioResourceService
#         get_assoc = ScenarioResourceService.get_resource_by_id(
#             account_id=account_id, resource_type=resource_type, payload=get_payload
#         )

#         # Assert: Check if the assoc scenario ID is the same
#         assert origin_assoc.scenario.id == get_assoc.scenario.id

#         # Assert: Check if the assoc resource ID is the same
#         origin_resource = getattr(origin_assoc, resource_type).id
#         get_resource = getattr(get_assoc, resource_type).id

#         assert origin_resource == get_resource

#         # Assert: Ensure the returned ScenarioDomain matches the input payload
#         TestScenarioResourceServiceCase._assert_assoc_fields_with_another_assoc(
#             assoc=get_assoc, another_assoc=origin_assoc
#         )

#     @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
#     def test_update_resource_through_scenario_resource_service(
#         self, default_account, default_scenario, resource_type
#     ):
#         """Test updating a resource to given scenario with given account using ScenarioResourceService"""

#         # Arrange: Getting account and scenario id
#         account_id, scenario_id = default_account.id, default_scenario.id

#         # Arrange: Create a resource based on the resource_type
#         resource_id = TestScenarioResourceServiceCase._create_resource(
#             default_account, resource_type
#         )

#         # Arrange: Add resource to given scenario by given account
#         TestScenarioResourceServiceCase._add_resource_to_scenario(
#             account_id=account_id,
#             scenario_id=scenario_id,
#             resource_id=resource_id,
#             resource_type=resource_type,
#         )

#         # Arrange: Create the update payload
#         updated_field = {
#             "memo": "This is the updated memo. For testing updated scenario resource service.",
#         }
#         updated_payload = {
#             "scenario_id": scenario_id,
#             **{f"{resource_type}_id": resource_id},
#             **updated_field,
#         }

#         # Act: Update the resource by ScenarioResourceService
#         updated_assoc = ScenarioResourceService.update_resource_by_id(
#             account_id=account_id, resource_type=resource_type, payload=updated_payload
#         )

#         # Assert: Check if the update is successful
#         for field in updated_field.keys():
#             assoc_value = getattr(updated_assoc, field)
#             expected_value = updated_payload[field]
#             assert (
#                 assoc_value == expected_value
#             ), f"Return Assoc field '{field}' is '{assoc_value}', not '{expected_value}'"
