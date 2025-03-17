# from app.domain.entities import IncomeDomain


class TestIncomeDomainCase:
    def test_create_income_domain(default_income_domain, default_account_domain):
        # Assert
        assert default_income_domain.name == "Default Income Domain"
        assert default_income_domain.amount == 50000
        assert default_income_domain.max_yearly_growth_rate == 0.5
        assert default_income_domain.min_yearly_growth_rate == -0.5
        assert default_income_domain.start_age == 20
        assert default_income_domain.owner_id == default_account_domain.id
