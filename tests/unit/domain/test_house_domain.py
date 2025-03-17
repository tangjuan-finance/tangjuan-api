# from app.domain.entities import HouseDomain


class TestHouseDomainCase:
    def test_create_house_domain(default_house_domain, default_account_domain):
        # Assert
        assert default_house_domain.name == "Default House Domain"
        assert default_house_domain.amount == 20000000
        assert default_house_domain.down_payment == 3000000
        assert default_house_domain.interest_rate == 3.0
        assert default_house_domain.loan_term == 40
        assert default_house_domain.purchase_age == 20
        assert default_house_domain.owner_id == default_account_domain.id
