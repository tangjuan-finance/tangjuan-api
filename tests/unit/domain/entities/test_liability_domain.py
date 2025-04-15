from app.domain.entities import LiabilityDomain
from decimal import Decimal
from tests.factory import LiabilityDomainFactory


class TestLiabilityDomainCase:
    def test_create_liability_domain(self, default_account_domain):
        # Arrange
        name = "Default Liability Domain"
        principal_amount = 50000
        interest_rate = Decimal("0.5")
        start_age = 20
        end_age = 50

        # Act
        liability = LiabilityDomain(
            name=name,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            start_age=start_age,
            end_age=end_age,
            owner=default_account_domain,
        )

        # Assert
        assert isinstance(liability.id, str)
        assert len(liability.id) == 13
        assert liability.name == name
        assert liability.principal_amount == principal_amount
        assert liability.interest_rate == interest_rate
        assert liability.start_age == start_age
        assert liability.end_age == end_age
        assert liability.owner == default_account_domain

    def test_factory_liability_domain(self):
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
        assert isinstance(liability.id, str)
        assert len(liability.id) == 13
        assert liability.name == name
        assert liability.principal_amount == principal_amount
        assert liability.interest_rate == interest_rate
        assert liability.start_age == start_age
        assert liability.end_age == end_age
