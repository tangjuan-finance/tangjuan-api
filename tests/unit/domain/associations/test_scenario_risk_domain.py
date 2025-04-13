# from app.domain.entities import RiskDomain
from app.domain.associations import ScenarioRiskDomain
from tests.factory import create_fake_id
from datetime import datetime, timezone
from decimal import Decimal


class TestRiskDomainCase:
    def test_create_scenario_risk_domain(self):
        # Arrange
        scenario_id = create_fake_id()
        risk_id = create_fake_id()
        probability = Decimal("0.4")
        # Act
        scenario_risk = ScenarioRiskDomain(
            scenario_id=scenario_id,
            risk_id=risk_id,
            probability=probability,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        # Assert
        assert scenario_risk.scenario_id == scenario_id
        assert scenario_risk.risk_id == risk_id
        assert scenario_risk.probability == probability
