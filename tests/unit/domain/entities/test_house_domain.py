# from app.domain.entities import HouseDomain
from decimal import Decimal
from tests.unit.factories import HouseDomainFactory


class TestHouseDomainCase:
    def test_create_house_domain(default_house_domain, default_account_domain):
        # Assert
        assert default_house_domain.name == "Default House Domain"
        assert default_house_domain.amount == 20000000
        assert default_house_domain.down_payment == 3000000
        assert default_house_domain.interest_rate == Decimal("3")
        assert default_house_domain.loan_term == 40
        assert default_house_domain.purchase_age == 20
        assert default_house_domain.owner_id == default_account_domain.id

    def test_factory_house_domain():
        # Arrange
        name = "Default House Domain"
        amount = 20000000
        down_payment = 3000000
        interest_rate = Decimal("3")
        loan_term = 40
        purchase_age = 20

        # Act
        house = HouseDomainFactory(
            name=name,
            amount=amount,
            down_payment=down_payment,
            interest_rate=interest_rate,
            loan_term=loan_term,
            purchase_age=purchase_age,
        )

        # Assert
        assert house.name == name
        assert house.amount == amount
        assert house.down_payment == down_payment
        assert house.interest_rate == interest_rate
        assert house.loan_term == loan_term
        assert house.purchase_age == purchase_age
