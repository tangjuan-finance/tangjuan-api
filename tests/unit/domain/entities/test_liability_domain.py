# from app.domain.entities import LiabilityDomain
from decimal import Decimal
from tests.unit.factories import LiabilityDomainFactory


class TestLiabilityDomainCase:
    def test_create_liability_domain(default_liability_domain, default_account_domain):
        # Assert
        assert default_liability_domain.name == "Default Liability Domain"
        assert default_liability_domain.principal_amount == 50000
        assert default_liability_domain.interest_rate == Decimal("0.5")
        assert default_liability_domain.start_age == 20
        assert default_liability_domain.end_age == 50
        assert default_liability_domain.owner_id == default_account_domain.id

    def test_factory_liability_domain():
        # Arrange
        name = "Default Liability Domain"
        principal_amount = 50000
        interest_rate = Decimal("0.5")
        start_age = 20
        end_age = 50

        # Act
        liability = LiabilityDomainFactory(
            name=name,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert liability.name == name
        assert liability.principal_amount == principal_amount
        assert liability.interest_rate == interest_rate
        assert liability.start_age == start_age
        assert liability.end_age == end_age
