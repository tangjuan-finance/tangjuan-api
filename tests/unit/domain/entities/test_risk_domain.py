# from app.domain.entities import RiskDomain
from tests.factory import RiskDomainFactory


class TestRiskDomainCase:
    def test_factory_risk_domain(self):
        # Arrange
        name = "Default Risk Domain"
        max_loss = 100000
        min_loss = 50000
        start_age = 20
        end_age = 30

        # Act
        risk = RiskDomainFactory(
            name=name,
            max_loss=max_loss,
            min_loss=min_loss,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert risk.name == name
        assert risk.max_loss == max_loss
        assert risk.min_loss == min_loss
        assert risk.start_age == start_age
