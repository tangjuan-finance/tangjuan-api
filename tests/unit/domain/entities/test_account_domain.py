class TestAccountDomainCase:
    def test_default_account_domain(default_account_domain):
        # Assert
        assert default_account_domain.username == "default"
        assert default_account_domain.email == "default@example.com"
        assert default_account_domain.check_password("default$ercet")
