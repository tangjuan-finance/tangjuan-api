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
from app.domain.entity import (
    ExpenseDomain,
    IncomeDomain,
    HouseDomain,
    ChildDomain,
    RiskDomain,
    AssetDomain,
    LiabilityDomain,
)


class TestScenarioDomainCase:
    def test_create_scenario_domain(default_scenario_domain, default_account_domain):
        # Assert
        assert default_scenario_domain.name == "Default Scenario Domain"
        assert default_scenario_domain.scenario_allocation_percentage == Decimal("0.7")
        assert default_scenario_domain.retire_age == 20
        assert default_scenario_domain.owner_id == default_account_domain.id

    def test_factory_scenario_domain():
        # Arrange
        name = "Default Scenario Domain"
        scenario_allocation_percentage = Decimal("0.7")
        retire_age = 20

        # Act
        scenario = ScenarioDomainFactory(
            name=name,
            scenario_allocation_percentage=scenario_allocation_percentage,
            retire_age=retire_age,
        )

        # Assert
        assert scenario.name == name
        assert scenario.scenario_allocation_percentage == scenario_allocation_percentage
        assert scenario.retire_age == retire_age

    @pytest.mark.parametrize(
        "resource_factory, resource_attr, resource_class, resource_field, resource_data, update_data",
        [
            (
                ExpenseDomainFactory,
                "expenses",
                ExpenseDomain,
                "max_yearly_growth_rate",
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),
            (
                IncomeDomainFactory,
                "incomes",
                IncomeDomain,
                "max_yearly_growth_rate",
                {"max_yearly_growth_rate": Decimal("0.2")},
                {"max_yearly_growth_rate": Decimal("0.7")},
            ),  # No specific field
            (
                HouseDomainFactory,
                "houses",
                HouseDomain,
                "interest_rate",
                {"interest_rate": Decimal("3.0")},
                {"interest_rate": Decimal("5.0")},
            ),  # No specific field
            (
                ChildDomainFactory,
                "children",
                ChildDomain,
                "birth_age",
                {"birth_age": 34},
                {"birth_age": 26},
            ),
            (
                RiskDomainFactory,
                "risks",
                RiskDomain,
                "max_loss",
                {"max_loss": 100000},
                {"max_loss": 500000},
            ),
            (
                AssetDomainFactory,
                "assets",
                AssetDomain,
                "max_yearly_return_rate",
                {"max_yearly_return_rate": Decimal("0.2")},
                {"max_yearly_return_rate": Decimal("0.7")},
            ),
            (
                LiabilityDomainFactory,
                "liabilities",
                LiabilityDomain,
                "interest_rate",
                {"interest_rate": Decimal("0.5")},
                {"interest_rate": Decimal("0.7")},
            ),
        ],
    )
    def test_add_resource_to_scenario_domain(
        default_scenario_domain,
        resource_factory,
        resource_attr,
        resource_class,
        resource_field,
        resource_data,
        update_data,
    ):
        # Arrange
        resource_instance = (
            resource_factory()
        )  # Use the factory to generate the resource with the data

        # Act: Add an expense to the scenario
        default_scenario_domain.add_resource(resource_instance, **resource_data)

        # Assert: Ensure the expense is added and amount is correct
        assert resource_instance in getattr(default_scenario_domain, resource_attr)
        assert (
            getattr(getattr(default_scenario_domain, resource_attr)[0], resource_field)
            == resource_data[resource_field]
        )

        # Act: Get expense id
        resource_id = resource_instance.id

        # Assert: Could retrieve expense by id
        assert (
            default_scenario_domain.get_resource_by_id(resource_class, resource_id)
            == resource_instance
        )

        # Act: Update the expense amount
        default_scenario_domain.update_resource(resource_instance, **update_data)

        # Assert: Ensure the expense amount is updated correctly
        assert (
            getattr(getattr(default_scenario_domain, resource_attr)[0], resource_field)
            == update_data[resource_field]
        )

        # Act: Delete the expense
        default_scenario_domain.delete_resource(resource_instance)

        # Assert: Ensure the expense is removed from the scenario
        assert len(getattr(default_scenario_domain, resource_attr)) == 0
