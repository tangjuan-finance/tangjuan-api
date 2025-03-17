# from app.domain.entities import ScenarioDomain


class TestScenarioDomainCase:
    def test_create_scenario_domain(default_scenario_domain, default_account_domain):
        # Assert
        assert default_scenario_domain.name == "Default Scenario Domain"
        assert default_scenario_domain.asset_allocation_percentage == 0.7
        assert default_scenario_domain.retire_age == 20
        assert default_scenario_domain.owner_id == default_account_domain.id
