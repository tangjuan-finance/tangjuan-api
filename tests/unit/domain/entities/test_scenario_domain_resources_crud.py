# from app.domain.entities import ScenarioDomain
import pytest
from decimal import Decimal
from types import MappingProxyType
from tests.unit.factories import (
    ExpenseDomainFactory,
    IncomeDomainFactory,
    HouseDomainFactory,
    ChildDomainFactory,
    RiskDomainFactory,
    AssetDomainFactory,
    LiabilityDomainFactory,
    ScenarioDomainFactory,
)

from app.domain.associations import (
    ScenarioExpenseDomain,
    ScenarioIncomeDomain,
    ScenarioHouseDomain,
    ScenarioChildDomain,
    ScenarioRiskDomain,
    ScenarioAssetDomain,
    ScenarioLiabilityDomain,
    BaseAssociationDomain,
)
from datetime import datetime, timezone
from app.domain.entities import ScenarioDomain
from app.mapper.resource_mapper import ResourceMapper
from nanoid import generate

resource_param = {
    "param": "resource_type, resource_field, resource_data, update_data",
    "payload": [
        (
            "expense",
            "max_yearly_growth_rate",
            {"max_yearly_growth_rate": Decimal("0.2")},
            {"max_yearly_growth_rate": Decimal("0.7")},
        ),
        (
            "income",
            "max_yearly_growth_rate",
            {"max_yearly_growth_rate": Decimal("0.2")},
            {"max_yearly_growth_rate": Decimal("0.7")},
        ),
        (
            "house",
            "interest_rate",
            {"interest_rate": Decimal("3.0")},
            {"interest_rate": Decimal("5.0")},
        ),
        (
            "child",
            "birth_age",
            {"birth_age": 34},
            {"birth_age": 26},
        ),
        (
            "risk",
            "max_loss",
            {"max_loss": 100000},
            {"max_loss": 500000},
        ),
        (
            "asset",
            "allocation_percentage",
            {"allocation_percentage": Decimal("0.2")},
            {"allocation_percentage": Decimal("0.7")},
        ),
        (
            "liability",
            "allocation_percentage",
            {"allocation_percentage": Decimal("0.5")},
            {"allocation_percentage": Decimal("0.7")},
        ),
    ],
}


class TestScenarioDomainResourcesCrudCase:
    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Get resource collection
        resource_collection = self._get_collection_from_resource_type(
            scenario=default_scenario_domain, resource_type=resource_type
        )

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Act: Add the resource to the scenario
        default_scenario_domain._add_association(resource_association)

        # Arrange: Retrieve the association
        assoc_from_collection = self._get_assoc_from_collection(
            collection=resource_collection,
            resource_type=resource_type,
            resource_id=resource_id,
        )

        # Assert: Association from collection matches the expected resource_association
        assert assoc_from_collection == resource_association

        # Assert: Resource field in the association is correctly set
        assert (
            getattr(assoc_from_collection, resource_field)
            == resource_data[resource_field]
        )

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_resource_from_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Act: Add the resource to the scenario
        default_scenario_domain._add_association(resource_association)

        # Assert: Ensure association can be retrieved by resource instance
        retrieved_association = default_scenario_domain.get_association_by_resource_id(
            resource_type=resource_type, resource_id=resource_id
        )
        assert retrieved_association == resource_association

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_update_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Get resource collection
        resource_collection = self._get_collection_from_resource_type(
            scenario=default_scenario_domain, resource_type=resource_type
        )

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Arrange: Add the resource to the scenario
        default_scenario_domain._add_association(resource_association)

        # Act: Update the resource data in the association
        default_scenario_domain._update_association(resource_association, **update_data)

        # Arrange: Retrieve the association
        updated_assoc = self._get_assoc_from_collection(
            collection=resource_collection,
            resource_type=resource_type,
            resource_id=resource_id,
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
    def test_remove_resource_from_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Arrange: Get resource collection
        resource_collection = self._get_collection_from_resource_type(
            scenario=default_scenario_domain, resource_type=resource_type
        )

        # Arrange: Add the resource to the scenario
        default_scenario_domain._add_association(resource_association)

        # Assert: Check if the assoc exist
        assoc_from_collection = self._get_assoc_from_collection(
            collection=resource_collection,
            resource_type=resource_type,
            resource_id=resource_id,
        )

        assert assoc_from_collection is not None

        # Act: Delete the resource from the scenario
        default_scenario_domain._delete_association(resource_association)

        # Assert: Ensure the resource is removed from the scenario domain
        deleted_assoc_from_collection = self._get_assoc_from_collection(
            collection=resource_collection,
            resource_type=resource_type,
            resource_id=resource_id,
        )

        assert deleted_assoc_from_collection is None

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_duplicate_resource_to_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Arrange: Add the resource to the scenario
        default_scenario_domain._add_association(resource_association)

        # Act: Add the resource twice should raise error
        with pytest.raises(ValueError):
            default_scenario_domain._add_association(resource_association)

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_add_resource_to_scenario_domain_passing_assoc_in_another_scenario(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Arrange: Create another scenario
        another_scenario = ScenarioDomainFactory()

        # Assert: Add the resource to the scenario by passing assoc in another scenario should raise ValueError
        with pytest.raises(ValueError):
            another_scenario._add_association(resource_association)

    def test_add_invalid_assoc_to_scenario_domain(
        self,
        default_scenario_domain,
    ):
        # Arrange: Create Resource
        resource = ExpenseDomainFactory()

        # Act: Add resource to the scenario by resource should raise TypeError as assoc is expected
        with pytest.raises(TypeError):
            default_scenario_domain._add_association(resource)

    def test_add_assoc_with_invalid_resource_type_to_scenario_domain(
        self,
        default_scenario_domain,
    ):
        # Arrange: Create Resource
        assoc_invalid_resource = BaseAssociationDomain(
            scenario_id=default_scenario_domain.id, memo="This is BaseAssociationDomain"
        )

        # Act: Add resource to the scenario by resource should raise TypeError as assoc is expected
        with pytest.raises(ValueError):
            default_scenario_domain._add_association(assoc_invalid_resource)

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_retrieve_not_existed_resource_from_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Generate Fake Resource ID
        resource_id = generate(size=13)

        # Assert: Ensure association can be retrieved by resource instance
        retrieved_association = default_scenario_domain.get_association_by_resource_id(
            resource_type=resource_type, resource_id=resource_id
        )
        assert retrieved_association is None

    @pytest.mark.parametrize(resource_param["param"], resource_param["payload"])
    def test_remove_not_existed_resource_from_scenario_domain(
        self,
        default_scenario_domain,
        resource_type,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange: Create Resource Domain and get Resource ID
        resource_id = self._create_resource_from_type(resource_type=resource_type)

        # Arrange: Create the resource association
        resource_association = self._create_resource_assoc(
            scenario_id=default_scenario_domain.id,
            resource_id=resource_id,
            resource_type=resource_type,
            **resource_data,
        )

        # Arrange: Get resource collection
        resource_collection = self._get_collection_from_resource_type(
            scenario=default_scenario_domain, resource_type=resource_type
        )

        # Assert: Ensure the assoc not exist
        assoc_from_collection = self._get_assoc_from_collection(
            collection=resource_collection,
            resource_type=resource_type,
            resource_id=resource_id,
        )

        assert assoc_from_collection is None

        # Act: Delete the non existant resource from the scenario will raise ValueError, so we know the resource is not in scenario as expected
        with pytest.raises(ValueError):
            default_scenario_domain._delete_association(resource_association)

    @staticmethod
    def _get_collection_from_resource_type(
        scenario: ScenarioDomain, resource_type: str
    ) -> BaseAssociationDomain:
        # Get collection name
        mapper = ResourceMapper.by_resource_type(resource_type)
        collection_name = mapper.collection_type

        # Get resource collection
        resource_collection = getattr(scenario, collection_name, None)
        if resource_collection is None:
            raise ValueError(f"{collection_name} are not existed.")

        return resource_collection

    @staticmethod
    def _get_assoc_from_collection(
        collection: list, resource_type: str, resource_id: str
    ) -> BaseAssociationDomain:
        # Retrieve the association using resource_instance from the collection
        assoc = [
            assoc
            for assoc in collection
            if getattr(assoc, f"{resource_type}_id") == resource_id
        ]

        if len(assoc) == 0:
            return None
        elif len(assoc) != 1:
            raise ValueError(
                f"{resource_type} with ID {resource_id} duplicated in the given collection."
            )
        else:
            return assoc[0]

    @staticmethod
    def _create_resource_from_type(resource_type: str) -> str:
        _RESOURCE_FACTORY_MAPPING = MappingProxyType(
            {
                "child": ChildDomainFactory,
                "liability": LiabilityDomainFactory,
                "expense": ExpenseDomainFactory,
                "income": IncomeDomainFactory,
                "house": HouseDomainFactory,
                "risk": RiskDomainFactory,
                "asset": AssetDomainFactory,
            }
        )

        # Generate resource instance through resource factory mapping by resource type
        resource_instance = _RESOURCE_FACTORY_MAPPING[resource_type]()
        if not resource_instance:
            raise ValueError(f"Could not create {resource_instance} association")

        return resource_instance.id

    @staticmethod
    def _create_resource_assoc(
        scenario_id: str,
        resource_id: str,
        resource_type: str,
        **resource_data: dict,
    ) -> BaseAssociationDomain:
        _ASSOC_CLS_MAPPING = MappingProxyType(
            {
                "child": ScenarioChildDomain,
                "liability": ScenarioLiabilityDomain,
                "expense": ScenarioExpenseDomain,
                "income": ScenarioIncomeDomain,
                "house": ScenarioHouseDomain,
                "risk": ScenarioRiskDomain,
                "asset": ScenarioAssetDomain,
            }
        )
        # Generate Resource Assoc Class
        resource_association_cls = _ASSOC_CLS_MAPPING[resource_type]

        resource_association = resource_association_cls(
            scenario_id=scenario_id,
            **{f"{resource_type}_id": resource_id},
            **resource_data,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        if not resource_association:
            raise ValueError(f"Could not create {resource_type} association")

        return resource_association
