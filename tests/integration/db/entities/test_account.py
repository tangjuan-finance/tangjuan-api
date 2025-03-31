from app import db
from app.infrastructure.models import Account
import sqlalchemy as sa
from ..factories import create_account
from werkzeug.security import check_password_hash


class TestAccountModelCase:
    def test_default_account_domain(self, default_account_domain):
        assert isinstance(default_account_domain, Account)

        # Act
        default_user_from_db = db.session.scalar(
            sa.select(Account).where(Account.name == default_account_domain.name)
        )

        # Assert
        assert default_account_domain == default_user_from_db

    def test_create_account(self):
        # Arrange
        name = "alice"
        email = "alice@example.com"
        password = "bird"

        account = create_account(name=name, email=email, password=password)

        # Act
        account_from_db = db.session.scalar(
            sa.select(Account).where(Account.name == account.name)
        )
        # Assert
        assert account_from_db.name == account.name
        assert account_from_db.email == account.email
        assert check_password_hash(account_from_db.password_hash, password)

    def test_create_user_in_CJK(self):
        # Arrange
        name = "使用者"
        email = "user@example.com"
        password = "cat"

        user = create_account(name=name, email=email, password=password)

        # Act
        user_from_db = db.session.scalar(
            sa.select(Account).where(Account.name == user.name)
        )

        # Assert
        assert user_from_db.name == name

    def test_avatar(self):
        u = Account(name="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )


class TestAccountOwnershipModelCase:
    def test_avatar(self):
        u = Account(name="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )
