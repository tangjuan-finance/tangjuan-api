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
            sa.select(Account).where(
                Account.username == default_account_domain.username
            )
        )

        # Assert
        assert default_account_domain == default_user_from_db

    def test_create_account(self):
        # Arrange
        username = "alice"
        email = "alice@example.com"
        password = "bird"

        account = create_account(username=username, email=email, password=password)

        # Act
        account_from_db = db.session.scalar(
            sa.select(Account).where(Account.username == account.username)
        )
        # Assert
        assert account_from_db.username == account.username
        assert account_from_db.email == account.email
        assert check_password_hash(account_from_db.password_hash, password)

    def test_create_user_in_CJK(self):
        # Arrange
        username = "使用者"
        email = "user@example.com"
        password = "cat"

        user = create_account(username=username, email=email, password=password)

        # Act
        user_from_db = db.session.scalar(
            sa.select(Account).where(Account.username == user.username)
        )

        # Assert
        assert user_from_db.username == username

    def test_avatar(self):
        u = Account(username="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )


class TestAccountOwnershipModelCase:
    def test_avatar(self):
        u = Account(username="john", email="john@example.com")
        assert u.avatar(128) == (
            "https://www.gravatar.com/avatar/"
            "d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )
