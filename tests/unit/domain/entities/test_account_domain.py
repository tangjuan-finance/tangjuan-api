from tests.unit.factories import AccountDomainFactory


class TestAccountDomainCase:
    def test_default_account_domain(default_account_domain):
        # Assert
        assert default_account_domain.username == "default"
        assert default_account_domain.email == "default@example.com"
        assert default_account_domain.check_password("default$ercet")

    def test_factory_account_domain():
        # Arrange
        username = "default"
        email = "default@example.com"
        password = "default$ercet"

        # Act
        account = AccountDomainFactory(
            username="default",
            email="default@example.com",
        )

        account.set_password(password)

        # Assert
        assert account.username == username
        assert account.email == email
        assert account.check_password(password)
