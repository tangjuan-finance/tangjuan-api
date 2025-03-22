from tests.unit.factories import AccountDomainFactory
from werkzeug.security import generate_password_hash, check_password_hash


class TestAccountDomainCase:
    def test_default_account_domain(self, default_account_domain):
        # Assert
        assert default_account_domain.username == "default"
        assert default_account_domain.email == "default@example.com"
        assert check_password_hash(
            default_account_domain.password_hash, "default$ercet"
        )

    def test_factory_account_domain(self):
        # Arrange
        username = "default"
        email = "default@example.com"
        password = "default$ercet"
        password_hash = generate_password_hash(password)

        # Act
        account = AccountDomainFactory(
            username=username, email=email, password_hash=password_hash
        )

        # Assert
        assert account.username == username
        assert account.email == email
        assert account.password_hash == password_hash
