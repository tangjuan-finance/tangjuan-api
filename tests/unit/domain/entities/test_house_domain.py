from app.domain.entities import HouseDomain
from decimal import Decimal
from tests.factory import HouseDomainFactory


class TestHouseDomainCase:
    def test_create_house_domain(self, default_account_domain):
        # Arrange
        name = "Default House Domain"
        amount = 20000000
        down_payment = 3000000
        interest_rate = Decimal("3")
        loan_term = 40
        purchase_age = 20
        sale_age = 40

        # Act
        house = HouseDomain(
            name=name,
            amount=amount,
            down_payment=down_payment,
            interest_rate=interest_rate,
            loan_term=loan_term,
            purchase_age=purchase_age,
            sale_age=sale_age,
            owner=default_account_domain,
        )

        # Assert
        assert isinstance(house.id, str)
        assert len(house.id) == 13
        assert house.name == name
        assert house.amount == amount
        assert house.down_payment == down_payment
        assert house.interest_rate == interest_rate
        assert house.loan_term == loan_term
        assert house.purchase_age == purchase_age
        assert house.owner == default_account_domain

    def test_factory_house_domain(self):
        # Arrange
        name = "Default House Domain"
        amount = 20000000
        down_payment = 3000000
        interest_rate = Decimal("3")
        loan_term = 40
        purchase_age = 20
        sale_age = 40

        # Act
        house = HouseDomainFactory(
            name=name,
            amount=amount,
            down_payment=down_payment,
            interest_rate=interest_rate,
            loan_term=loan_term,
            purchase_age=purchase_age,
            sale_age=sale_age,
        )

        # Assert
        assert isinstance(house.id, str)
        assert len(house.id) == 13
        assert house.name == name
        assert house.amount == amount
        assert house.down_payment == down_payment
        assert house.interest_rate == interest_rate
        assert house.loan_term == loan_term
        assert house.purchase_age == purchase_age
