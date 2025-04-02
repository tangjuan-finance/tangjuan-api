# from app.domain.entities import RiskDomain
from app.domain.associations import ScenarioRiskDomain
from tests.factory import RiskDomainFactory
from datetime import datetime, timezone


class TestRiskDomainCase:
    def test_create_scenario_risk_domain(self, default_scenario_domain):
        # Arrange
        name = "risk for scenario"

        default_max_loss = 100000
        risk = RiskDomainFactory(name=name, max_loss=default_max_loss)
        max_loss = 500000
        # Act
        scenario_risk = ScenarioRiskDomain(
            scenario_id=default_scenario_domain.id,
            risk_id=risk.id,
            max_loss=max_loss,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_risk.scenario_id == default_scenario_domain.id
        assert scenario_risk.risk_id == risk.id
        assert scenario_risk.max_loss != default_max_loss
        assert scenario_risk.max_loss == max_loss
