# from app.domain.entities import RiskDomain
from tests.unit.factories import RiskDomainFactory


class TestRiskDomainCase:
    def test_create_risk_domain(default_risk_domain, default_account_domain):
        # Assert
        assert default_risk_domain.name == "Default Risk Domain"
        assert default_risk_domain.max_loss == 100000
        assert default_risk_domain.min_loss == 50000
        assert default_risk_domain.start_age == 20
        assert default_risk_domain.owner_id == default_account_domain.id

    def test_factory_risk_domain():
        # Arrange
        name = "Default Risk Domain"
        max_loss = 100000
        min_loss = 50000
        start_age = 20

        # Act
        risk = RiskDomainFactory(
            name=name,
            max_loss=max_loss,
            min_loss=min_loss,
            start_age=start_age,
        )

        # Assert
        assert risk.name == name
        assert risk.max_loss == max_loss
        assert risk.min_loss == min_loss
        assert risk.start_age == start_age
