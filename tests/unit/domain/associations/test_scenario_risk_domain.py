# from app.domain.entities import RiskDomain


class TestRiskDomainCase:
    def test_create_risk_domain(default_risk_domain, default_account_domain):
        # Assert
        assert default_risk_domain.name == "Default Risk Domain"
        assert default_risk_domain.max_loss == 100000
        assert default_risk_domain.min_loss == 50000
        assert default_risk_domain.start_age == 20
        assert default_risk_domain.owner_id == default_account_domain.id
