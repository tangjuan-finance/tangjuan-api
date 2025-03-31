import pytest
from app.repository.entities import ScenarioRepo
from decimal import Decimal
from app import db
import sqlalchemy as sa
from tests.unit.repo.factories import (
    create_expense,
    create_income,
    create_house,
    create_child,
    create_risk,
    create_asset,
    create_liability,
)
from app.mapper.resource_mapper import ResourceMapper


class TestScenarioRepoResourcesCrudCase:
    resource_param = {
        "param": "resource_name, resource_factory, resource_data, update_data",
        "payload": [
            (
                "expense",
                create_expense,
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),
            (
                "income",
                create_income,
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),
            (
                "house",
                create_house,
                {"interest_rate": Decimal("3.0")},
                {"interest_rate": Decimal("5.0")},
            ),  # No specific field
            (
                "child",
                create_child,
                {"birth_age": 34},
                {"birth_age": 26},
            ),
            (
                "risk",
                create_risk,
                {"max_loss": 100000},
                {"max_loss": 500000},
            ),
            (
                "asset",
                create_asset,
                {"allocation_percentage": Decimal("0.2")},
                {"allocation_percentage": Decimal("0.7")},
            ),
            (
                "liability",
                create_liability,
                {"allocation_percentage": Decimal("0.5")},
                {"allocation_percentage": Decimal("0.7")},
            ),
        ],
    }

    @staticmethod
    def _add_resource_to_scenario(resource, scenario, **resource_data):
        # Act: Add Expense to Scenario by ScenarioRepo
        return ScenarioRepo.add_resource(
            scenario=scenario, resource=resource, **resource_data
        )

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_to_scenario_by_repo(
        self,
        new_scenario,
        default_account,
        resource_name,
        resource_factory,
        resource_data,
        update_data,
    ):
        # Arrange: Creating Scenario and Resources
        resource = resource_factory(default_account)

        # Act: Add Expense to Scenario by ScenarioRepo
        assoc_from_repo = ScenarioRepo.add_resource(
            scenario=new_scenario, resource=resource, **resource_data
        )

        # Assert: Ensure the assoc are config as given
        assoc_resource = getattr(assoc_from_repo, resource_name)
        assert assoc_resource == resource
        assert assoc_from_repo.scenario == new_scenario

        for k, v in resource_data.items():
            assoc_attr = getattr(assoc_from_repo, k)
            assert assoc_attr == v

        # Assert: Ensure the assoc are stored in database
        mapper = ResourceMapper.from_assoc(assoc_from_repo)
        assoc_model = mapper.assoc_model_cls

        assoc_from_db = db.session.scalars(
            sa.select(assoc_model).where(
                (assoc_model.scenario_id == new_scenario.id)
                & (getattr(assoc_model, f"{resource_name}_id") == resource.id)
            )
        ).first()

        assert assoc_from_db is not None  # Ensure record exists

        # Assert: Ensure the assoc from database config the same as the repo one
        for k, v in resource_data.items():
            assoc_attr_from_repo = getattr(assoc_from_repo, k)
            assoc_attr_from_db = getattr(assoc_from_db, k)

            assert assoc_attr_from_repo == assoc_attr_from_db

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_by_id_from_scenario_repo(
        self,
        new_scenario,
        default_account,
        resource_name,
        resource_factory,
        resource_data,
        update_data,
    ):
        # Arrange: Creating Scenario and Resources
        resource = resource_factory(default_account)

        # Arrange: Adding resource to scenario by id
        assoc_from_repo = self._add_resource_to_scenario(
            resource, new_scenario, **resource_data
        )

        # Act: Get resource from scenario repo by id
        mapper = ResourceMapper.from_domain(resource)
        resource_domain = mapper.resource_domain_cls

        assoc_get_by_id = ScenarioRepo.get_resource_by_id(
            scenario=new_scenario,
            resource_type=resource_domain,
            resource_id=resource.id,
        )

        # Assert: Assert the assoc from get_resource_by_id is the same as assoc_from_repo
        assoc_resource_from_repo = getattr(assoc_from_repo, resource_name)
        assoc_resource_by_id = getattr(assoc_get_by_id, resource_name)
        assert assoc_resource_from_repo == assoc_resource_by_id
        assert assoc_get_by_id.scenario.id == assoc_from_repo.scenario.id

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_list_from_scenario_repo(
        self,
        new_scenario,
        default_account,
        resource_name,
        resource_factory,
        resource_data,
        update_data,
    ):
        # Arrange: Get resource domain class
        mapper = ResourceMapper.by_resource_type(resource_name)
        resource_domain = mapper.resource_domain_cls

        # Arrange: Get the origin length of the collection
        origin_len = len(
            ScenarioRepo.get_resource_list(
                scenario=new_scenario, resource_type=resource_domain
            )
        )

        # Arrange: Create 5 new assoc
        resource_list = [resource_factory(default_account) for _ in range(5)]
        for res in resource_list:
            self._add_resource_to_scenario(res, new_scenario, **resource_data)

        # Act: Get resource list
        assoc_list = ScenarioRepo.get_resource_list(
            scenario=new_scenario, resource_type=resource_domain
        )

        # Assert: Assert the assoc list
        for assoc in assoc_list:
            assert assoc.scenario.id == new_scenario.id
            assoc_res = getattr(assoc, resource_name)
            assert assoc_res in resource_list

        # Assert: Assert the assoc list and its length
        updated_len = len(assoc_list)
        assert updated_len == origin_len + 5

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_update_resource_to_scenario_repo(
        self,
        new_scenario,
        default_account,
        resource_name,
        resource_factory,
        resource_data,
        update_data,
    ):
        # Arrange: Create an Scenario Resource Assoc with default attr
        resource = resource_factory(default_account)

        ScenarioRepo.add_resource(
            scenario=new_scenario, resource=resource, **resource_data
        )

        # Act: Update the max_yearly_growth_rate
        updated_assoc = ScenarioRepo.update_resource(
            scenario=new_scenario, resource=resource, **update_data
        )

        # Assert: Ensure the update is successfully by checking the update_assoc attrs
        for k, v in update_data.items():
            assoc_attr = getattr(updated_assoc, k)
            assert assoc_attr == v

        # Assert: Ensure the assoc are stored in database
        mapper = ResourceMapper.from_assoc(updated_assoc)
        assoc_model = mapper.assoc_model_cls

        assoc_from_db = db.session.scalars(
            sa.select(assoc_model).where(
                (assoc_model.scenario_id == new_scenario.id)
                & (getattr(assoc_model, f"{resource_name}_id") == resource.id)
            )
        ).first()

        assert assoc_from_db is not None  # Ensure record exists

        # Assert: Ensure the assoc from database config the same as the repo one
        for k, v in update_data.items():
            assoc_attr_from_repo = getattr(updated_assoc, k)
            assoc_attr_from_db = getattr(assoc_from_db, k)

            assert assoc_attr_from_repo == assoc_attr_from_db

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_remove_resource_from_scenario_repo(
        self,
        new_scenario,
        default_account,
        resource_name,
        resource_factory,
        resource_data,
        update_data,
    ):
        # Arrange: Create an Scenario Resource Assoc with default attr
        resource = resource_factory(default_account)

        # Arrange: Adding resource to scenario by id
        self._add_resource_to_scenario(resource, new_scenario, **resource_data)

        # Arrange: Get Resource Domain
        mapper = ResourceMapper.from_domain(resource)
        resource_domain = mapper.resource_domain_cls

        # Act: Delete the assoc from the scenario by repo
        ScenarioRepo.remove_resource(
            scenario=new_scenario,
            resource_type=resource_domain,
            resource_id=resource.id,
        )

        # Assert: Check if assoc is deleted from repo
        assoc_from_repo = ScenarioRepo.get_resource_by_id(
            scenario=new_scenario,
            resource_type=resource_domain,
            resource_id=resource.id,
        )
        assert assoc_from_repo is None

        # Assert: Check if assoc is deleted from database

        assoc_model = mapper.assoc_model_cls

        assoc_from_db = db.session.scalars(
            sa.select(assoc_model).where(
                (assoc_model.scenario_id == new_scenario.id)
                & (getattr(assoc_model, f"{resource_name}_id") == resource.id)
            )
        ).first()
        assert assoc_from_db is None
