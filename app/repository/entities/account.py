# from dataclasses import dataclass
# from .base import EntityRepo
# from datetime import datetime


# @dataclass(kw_only=True)
# class AccountRepo(EntityRepo):
#     username: str
#     email: str
#     password_hash: str
#     last_seen: datetime

from app.domain.entities import AccountDomain
from app.infrastructure.models import Account
from app import db
import sqlalchemy as sa


class AccountRepo:
    @staticmethod
    def create(account: AccountDomain) -> AccountDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        account_model = Account(
            username=account.username,
            email=account.email,
            password_hash=account.password_hash,
            last_seen=account.last_seen,
        )

        # Save the Account model to the database
        db.session.add(account_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return AccountDomain(
            id=account_model.id,
            username=account_model.username,
            email=account_model.email,
            password_hash=account_model.password_hash,
            last_seen=account_model.last_seen,
            created_at=account_model.created_at,
            updated_at=account_model.updated_at,
        )

    @staticmethod
    def save(account: AccountDomain) -> AccountDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get account_model from database
        account_model = db.session.scalar(
            sa.select(Account).where(Account.id == account.id)
        )
        if not account_model:
            raise ValueError("Account not found")

        # Update Account Model
        account_model.username = account.username
        account_model.email = account.email
        account_model.password_hash = account.password_hash
        account_model.last_seen = account.last_seen

        db.session.commit()
        # Return the domain object with attributes populated from the database
        return AccountDomain(
            id=account_model.id,
            username=account_model.username,
            email=account_model.email,
            password_hash=account_model.password_hash,
            last_seen=account_model.last_seen,
            created_at=account_model.created_at,
            updated_at=account_model.updated_at,
        )

    @staticmethod
    def get_by_id(account_id: int) -> AccountDomain | None:
        """Retrieve an account by ID and return as DomainObject."""
        # Get account_model from database
        account_model = db.session.scalar(
            sa.select(Account).where(Account.id == account_id)
        )
        if not account_model:
            return None

        return AccountDomain(
            id=account_model.id,
            username=account_model.username,
            email=account_model.email,
            password_hash=account_model.password_hash,
            last_seen=account_model.last_seen,
            created_at=account_model.created_at,
            updated_at=account_model.updated_at,
        )

    @staticmethod
    def get_list() -> list[AccountDomain]:
        """Retrieve all accounts and return as a list of DomainObjects."""
        account_model_list = db.session.scalars(sa.select(Account)).all()
        return [
            AccountDomain(
                id=exp.id,
                username=exp.username,
                email=exp.email,
                password_hash=exp.password_hash,
                last_seen=exp.last_seen,
                created_at=exp.created_at,
                updated_at=exp.updated_at,
            )
            for exp in account_model_list
        ]

    @staticmethod
    def delete_by_id(account_id: int) -> None:
        """Given an account ID, remove it from the database."""
        # Get account_model from database
        account_model = db.session.scalar(
            sa.select(Account).where(Account.id == account_id)
        )
        if account_model:
            db.session.delete(account_model)
            db.session.commit()

        return None
