# from app.domain.entities import IncomeDomain
from decimal import Decimal
from tests.unit.factories import IncomeDomainFactory


class TestIncomeDomainCase:
    def test_create_income_domain(self, default_income_domain, default_account_domain):
        # Assert
        assert default_income_domain.name == "Default Income Domain"
        assert default_income_domain.amount == 50000
        assert default_income_domain.max_yearly_growth_rate == Decimal("0.5")
        assert default_income_domain.min_yearly_growth_rate == Decimal("-0.5")
        assert default_income_domain.start_age == 20
        assert default_income_domain.owner == default_account_domain

    def test_factory_income_domain(self):
        # Arrange
        name = "Default Income Domain"
        amount = 50000
        max_yearly_growth_rate = Decimal("0.5")
        min_yearly_growth_rate = Decimal("-0.5")
        start_age = 20

        # Act
        income = IncomeDomainFactory(
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
        )

        # Assert
        assert income.name == name
        assert income.amount == amount
        assert income.max_yearly_growth_rate == max_yearly_growth_rate
        assert income.min_yearly_growth_rate == min_yearly_growth_rate
        assert income.start_age == start_age
