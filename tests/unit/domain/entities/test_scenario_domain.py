# from app.domain.entities import ScenarioDomain
from decimal import Decimal
from tests.factory import ScenarioDomainFactory


class TestScenarioDomainCase:
    def test_create_scenario_domain(
        self, default_scenario_domain, default_account_domain
    ):
        # Assert
        assert default_scenario_domain.name == "Default Scenario Domain"
        assert default_scenario_domain.asset_allocation_percentage == Decimal("0.7")
        assert default_scenario_domain.retire_age == 20
        assert default_scenario_domain.owner == default_account_domain

    def test_factory_scenario_domain(self):
        # Arrange
        name = "Default Scenario Domain"
        asset_allocation_percentage = Decimal("0.7")
        retire_age = 20

        # Act
        scenario = ScenarioDomainFactory(
            name=name,
            asset_allocation_percentage=asset_allocation_percentage,
            retire_age=retire_age,
        )

        # Assert
        assert scenario.name == name
        assert scenario.asset_allocation_percentage == asset_allocation_percentage
        assert scenario.retire_age == retire_age
