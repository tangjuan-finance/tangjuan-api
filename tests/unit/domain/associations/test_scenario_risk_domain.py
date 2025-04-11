# from app.domain.entities import RiskDomain
from app.domain.associations import ScenarioRiskDomain
from tests.factory import RiskDomainFactory
from datetime import datetime, timezone
from decimal import Decimal


class TestRiskDomainCase:
    def test_create_scenario_risk_domain(self, default_scenario_domain):
        # Arrange
        name = "risk for scenario"

        default_probability = Decimal("0.2")
        risk = RiskDomainFactory(name=name, probability=default_probability)
        probability = Decimal("0.4")
        # Act
        scenario_risk = ScenarioRiskDomain(
            scenario_id=default_scenario_domain.id,
            risk_id=risk.id,
            probability=probability,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_risk.scenario_id == default_scenario_domain.id
        assert scenario_risk.risk_id == risk.id
        assert scenario_risk.probability != default_probability
        assert scenario_risk.probability == probability
