from app.api.errors.bad_request import (
    UserNameDuplicationError,
    EmailDuplicationError,
    EmailFormatError,
)
from app.infrastructure.models import Account
from app import db
import sqlalchemy as sa
from cryptography.fernet import InvalidToken
from app.api.utils.encryption import decrypt_data
import re


def validate_username(username: str):
    """Check if username already exists."""
    account = db.session.scalar(sa.select(Account).where(Account.username == username))
    if account is not None:
        raise UserNameDuplicationError(errors={"username": "Username already taken"})


def validate_email_format(email: str):
    """Check if email format incorrect and already exists."""

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        raise EmailFormatError(errors={"email": "Invalid email format"})


def validate_email(email: str):
    """Check if email format incorrect and already exists."""

    account = db.session.scalar(sa.select(Account).where(Account.email == email))
    if account is not None:
        raise EmailDuplicationError(
            errors={"email": "Email address already registered"}
        )


def validate_token(token: str, mode: str):
    """Check if email already exists."""

    # If decrypt_data failed, InvalidToken get raised
    try:
        data = decrypt_data(token, mode=mode)
        return data
    except InvalidToken:
        raise InvalidToken
