# from app.domain.entities import LiabilityDomain
from decimal import Decimal


class TestLiabilityDomainCase:
    def test_create_liability_domain(default_liability_domain, default_account_domain):
        # Assert
        assert default_liability_domain.name == "Default Liability Domain"
        assert default_liability_domain.principal_amount == 50000
        assert default_liability_domain.interest_rate == Decimal("0.5")
        assert default_liability_domain.start_age == 20
        assert default_liability_domain.end_age == 50
        assert default_liability_domain.owner_id == default_account_domain.id
