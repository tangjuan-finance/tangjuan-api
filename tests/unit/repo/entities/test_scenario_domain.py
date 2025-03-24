# from app.domain.entities import ScenarioDomain
import pytest
from decimal import Decimal
from tests.unit.factories import (
    ScenarioDomainFactory,
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
)

from app.domain.associations import (
    ScenarioExpenseDomain,
    ScenarioIncomeDomain,
    ScenarioHouseDomain,
    ScenarioChildDomain,
    ScenarioRiskDomain,
    ScenarioAssetDomain,
    ScenarioLiabilityDomain,
)
from datetime import datetime, timezone
from app.repository.entities import ScenarioRepo
from app.infrastructure.models.entities import Scenario
import sqlalchemy as sa
from app import db


class TestScenarioDomainCase:
    def test_create_scenario_domain_through_repo(self):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory()

        # Act: Save the scenario domain using the repo and return the saved entity
        scenario_from_repo = ScenarioRepo.create(scenario)
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_from_repo.id == scenario_from_db.id
        assert scenario_from_repo.name == scenario_from_db.name
        assert (
            scenario_from_repo.asset_allocation_percentage
            == scenario_from_db.asset_allocation_percentage
        )
        assert scenario_from_repo.retire_age == scenario_from_db.retire_age
        assert scenario_from_repo.owner == scenario_from_db.owner
        assert scenario_from_repo.created_at == scenario_from_db.created_at
        assert scenario_from_repo.updated_at == scenario_from_db.updated_at

    def test_update_scenario_domain_through_repo(self):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory()
        scenario_from_repo = ScenarioRepo.create(scenario)
        updated_name = "Updated Scenario Domain"

        # Act: Update the scenario domain object (before saving)
        scenario_from_repo.name = updated_name

        # Save the updated object through the repository and get the result
        updated_scenario = ScenarioRepo.save(scenario_from_repo)

        # Query the database to verify the updated scenario record
        scenario_from_db = db.session.scalar(
            sa.select(Scenario).where(Scenario.id == scenario_from_repo.id)
        )

        # Assert: Ensure the values match between the domain object and the saved record
        assert updated_scenario.id == scenario_from_db.id
        assert updated_scenario.name == scenario_from_db.name
        assert updated_scenario.created_at == scenario_from_db.created_at
        assert updated_scenario.updated_at != scenario_from_db.updated_at

    def test_get_scenario_domain_by_id_through_repo(self):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory()
        ScenarioRepo.create(scenario)

        # Act: Update the scenario domain object (before saving)
        scenario_get_by_id = ScenarioRepo.get_by_id(scenario.id)

        # Assert: Ensure the values match between the domain object and the saved record
        assert scenario_get_by_id.id == scenario.id
        assert scenario_get_by_id.name == scenario.name

    def test_get_scenario_domain_list_through_repo(self):
        # Arrange: Create an scenario domain using the factory
        origin_scenario_list_length = len(ScenarioRepo.get_list())

        # Act: Create 5 new scenario domains
        for _ in range(5):
            scenario = ScenarioDomainFactory()
            ScenarioRepo.create(scenario)

        # Assert: Ensure the list length is increased by 5
        updated_scenario_list_length = len(ScenarioRepo.get_list())
        assert updated_scenario_list_length == (origin_scenario_list_length + 5)

    def test_delete_scenario_domain_through_repo(self):
        # Arrange: Create an scenario domain using the factory
        scenario = ScenarioDomainFactory()
        scenario_from_repo = ScenarioRepo.create(scenario)

        # Act: Delete the scenario domain object
        ScenarioRepo.delete(scenario_from_repo)

        # Assert: Ensure the scenario record is deleted from the database
        assert (
            db.session.scalar(
                sa.select(Scenario).where(Scenario.id == scenario_from_repo.id)
            )
            is None
        )

    resource_param = {
        "param": "resource_factory, resource_attr, resource_name, resource_association_cls, resource_field, resource_data, update_data",
        "payload": [
            (
                ExpenseDomainFactory,
                "expenses",
                "expense",
                ScenarioExpenseDomain,
                "max_yearly_growth_rate",
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),
            (
                IncomeDomainFactory,
                "incomes",
                "income",
                ScenarioIncomeDomain,
                "max_yearly_growth_rate",
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),  # No specific field
            (
                HouseDomainFactory,
                "houses",
                "house",
                ScenarioHouseDomain,
                "interest_rate",
                {"interest_rate": Decimal("3.0")},
                {"interest_rate": Decimal("5.0")},
            ),  # No specific field
            (
                ChildDomainFactory,
                "children",
                "child",
                ScenarioChildDomain,
                "birth_age",
                {"birth_age": 34},
                {"birth_age": 26},
            ),
            (
                RiskDomainFactory,
                "risks",
                "risk",
                ScenarioRiskDomain,
                "max_loss",
                {"max_loss": 100000},
                {"max_loss": 500000},
            ),
            (
                AssetDomainFactory,
                "assets",
                "asset",
                ScenarioAssetDomain,
                "allocation_percentage",
                {"allocation_percentage": Decimal("0.2")},
                {"allocation_percentage": Decimal("0.7")},
            ),
            (
                LiabilityDomainFactory,
                "liabilities",
                "liability",
                ScenarioLiabilityDomain,
                "allocation_percentage",
                {"allocation_percentage": Decimal("0.5")},
                {"allocation_percentage": Decimal("0.7")},
            ),
        ],
    }

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_factory,
        resource_attr,
        resource_name,
        resource_association_cls,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Generate the resource instance
        resource_instance = (
            resource_factory()
        )  # Use the factory to generate the resource with the data

        # Act: Add the resource to the scenario domain by creating and adding association
        resource_association = resource_association_cls(
            scenario=default_scenario_domain,
            **{resource_name: resource_instance},
            **resource_data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        default_scenario_domain._add_association(resource_association)

        # Assert: Ensure the resource has been correctly added to the scenario domain
        resource_collection = getattr(default_scenario_domain, resource_attr)

        # Retrieve the association using resource_instance from the collection
        assoc = next(
            (
                assoc
                for assoc in resource_collection
                if getattr(assoc, resource_name) == resource_instance
            ),
            None,
        )

        # Assert the association matches the expected resource_association
        assert assoc == resource_association

        # Assert that the resource field in the association is correctly set
        assert getattr(assoc, resource_field) == resource_data[resource_field]

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_factory,
        resource_attr,
        resource_name,
        resource_association_cls,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Generate the resource instance
        resource_instance = (
            resource_factory()
        )  # Use the factory to generate the resource with the data

        # Act: Add the resource to the scenario domain by creating and adding association
        resource_association = resource_association_cls(
            scenario=default_scenario_domain,
            **{resource_name: resource_instance},
            **resource_data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        default_scenario_domain._add_association(resource_association)

        # Assert: Ensure association can be retrieved by resource instance
        retrieved_association = default_scenario_domain.get_association_by_resource(
            resource_instance
        )
        assert retrieved_association == resource_association

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_update_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_factory,
        resource_attr,
        resource_name,
        resource_association_cls,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Generate the resource instance
        resource_instance = (
            resource_factory()
        )  # Use the factory to generate the resource with the data

        # Act: Add the resource to the scenario domain by creating and adding association
        resource_association = resource_association_cls(
            scenario=default_scenario_domain,
            **{resource_name: resource_instance},
            **resource_data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        default_scenario_domain._add_association(resource_association)
        resource_collection = getattr(default_scenario_domain, resource_attr)

        # Act: Update the resource data in the association
        default_scenario_domain._update_association(resource_association, **update_data)

        # Assert: Ensure the resource data is updated correctly
        updated_assoc = next(
            (assoc for assoc in resource_collection if assoc == resource_association),
            None,
        )

        # Assert that the updated association reflects the new field value
        assert (
            updated_assoc is not None
        ), "The association was not found in the collection"

        updated_field_value = getattr(updated_assoc, resource_field)
        assert (
            updated_field_value == update_data[resource_field]
        ), f"Expected {resource_field} to be {update_data[resource_field]}, but got {updated_field_value}"

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_delete_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_factory,
        resource_attr,
        resource_name,
        resource_association_cls,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Generate the resource instance
        resource_instance = (
            resource_factory()
        )  # Use the factory to generate the resource with the data

        # Act: Add the resource to the scenario domain by creating and adding association
        resource_association = resource_association_cls(
            scenario=default_scenario_domain,
            **{resource_name: resource_instance},
            **resource_data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        default_scenario_domain._add_association(resource_association)

        # Assert: Ensure the resource is removed from the scenario domain
        origin_length = len(getattr(default_scenario_domain, resource_attr))

        # Act: Delete the resource association from the scenario
        default_scenario_domain._delete_association(resource_association)

        # Assert: Ensure the resource is removed from the scenario domain
        updated_length = len(getattr(default_scenario_domain, resource_attr))
        assert updated_length == (
            origin_length - 1
        ), f"Expected collection length to decrease by 1, but got {updated_length}"
