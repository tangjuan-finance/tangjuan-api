from app.domain.entities import RiskDomain
from tests.factory import RiskDomainFactory
from decimal import Decimal


class TestRiskDomainCase:
    def test_create_risk_domain(self, default_account_domain):
        # Arrange
        name = "Default Risk Domain"
        amount = 100000
        probability = Decimal("0.1")
        start_age = 20
        end_age = 30

        # Act
        risk = RiskDomain(
            name=name,
            amount=amount,
            probability=probability,
            start_age=start_age,
            end_age=end_age,
            owner=default_account_domain,
        )

        # Assert
        assert isinstance(risk.id, str)
        assert len(risk.id) == 13
        assert risk.name == name
        assert risk.amount == amount
        assert risk.probability == probability
        assert risk.start_age == start_age
        assert risk.owner == default_account_domain

    def test_factory_risk_domain(self):
        # Arrange
        name = "Default Risk Domain"
        amount = 100000
        probability = Decimal("0.1")
        start_age = 20
        end_age = 30

        # Act
        risk = RiskDomainFactory(
            name=name,
            amount=amount,
            probability=probability,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert isinstance(risk.id, str)
        assert len(risk.id) == 13
        assert risk.name == name
        assert risk.amount == amount
        assert risk.probability == probability
        assert risk.start_age == start_age
