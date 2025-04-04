from tests.factory import AccountDomainFactory
from werkzeug.security import generate_password_hash


class TestAccountDomainCase:
    def test_factory_account_domain(self):
        # Arrange
        name = "default"
        email = "default@example.com"
        password = "default$ercet"
        password_hash = generate_password_hash(password)

        # Act
        account = AccountDomainFactory(
            name=name, email=email, password_hash=password_hash
        )

        # Assert
        assert account.name == name
        assert account.email == email
        assert account.password_hash == password_hash
