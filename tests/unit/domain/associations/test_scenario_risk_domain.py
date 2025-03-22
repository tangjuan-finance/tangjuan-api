# from app.domain.entities import RiskDomain
from app.domain.associations import ScenarioRiskDomain
from tests.unit.factories import RiskDomainFactory


class TestRiskDomainCase:
    def test_create_risk_domain(self):
        # Arrange
        default_max_loss = 100000
        risk = RiskDomainFactory(name="risk", max_loss=default_max_loss)
        max_loss = 500000
        # Act
        scenario_risk = ScenarioRiskDomain(
            risk=risk,
            max_loss=max_loss,
        )
        # Assert
        assert scenario_risk.risk.name == "risk"
        assert scenario_risk.max_loss != default_max_loss
        assert scenario_risk.max_loss == max_loss
