# from app.domain.entities import IncomeDomain
from decimal import Decimal
from tests.factory import IncomeDomainFactory


class TestIncomeDomainCase:
    def test_factory_income_domain(self):
        # Arrange
        name = "Default Income Domain"
        amount = 50000
        max_yearly_growth_rate = Decimal("0.5")
        min_yearly_growth_rate = Decimal("-0.5")
        start_age = 20
        end_age = 65
        # Act
        income = IncomeDomainFactory(
            name=name,
            amount=amount,
            max_yearly_growth_rate=max_yearly_growth_rate,
            min_yearly_growth_rate=min_yearly_growth_rate,
            start_age=start_age,
            end_age=end_age,
        )

        # Assert
        assert income.name == name
        assert income.amount == amount
        assert income.max_yearly_growth_rate == max_yearly_growth_rate
        assert income.min_yearly_growth_rate == min_yearly_growth_rate
        assert income.start_age == start_age
