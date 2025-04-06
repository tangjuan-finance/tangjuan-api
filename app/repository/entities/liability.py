from app.domain.entities import LiabilityDomain
from app.infrastructure.models import Liability, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class LiabilityRepo(EntityRepo):
    @staticmethod
    def create(liability: LiabilityDomain) -> LiabilityDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        liability_model = Liability(
            name=liability.name,
            principal_amount=liability.principal_amount,
            interest_rate=liability.interest_rate,
            start_age=liability.start_age,
            end_age=liability.end_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(liability_model, attr, getattr(liability, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == liability.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {liability.owner.id} not found")

        liability_model.owner = owner

        # Save the Liability model to the database
        db.session.add(liability_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return LiabilityRepo._map_to_domain(liability_model, owner.id)

    @staticmethod
    def save(liability: LiabilityDomain) -> LiabilityDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get liability_model from database
        liability_model = db.session.scalar(
            sa.select(Liability).where(Liability.id == liability.id)
        )
        if not liability_model:
            raise ValueError("Liability not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == liability.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {liability.owner.id} not found")

        # Update Liability Model
        liability_model.name = liability.name
        liability_model.principal_amount = liability.principal_amount
        liability_model.interest_rate = liability.interest_rate
        liability_model.start_age = liability.start_age
        liability_model.end_age = liability.end_age
        liability_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(liability_model, attr)
            setattr(liability_model, attr, getattr(liability, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return LiabilityRepo._map_to_domain(liability_model, owner.id)

    @staticmethod
    def get_by_id(liability_id: int) -> LiabilityDomain | None:
        """Retrieve an liability by ID and return as DomainObject."""
        # Get liability_model from database
        liability_model = db.session.scalar(
            sa.select(Liability).where(Liability.id == liability_id)
        )
        if not liability_model:
            return None

        # Return the domain object with attributes populated from the database
        return LiabilityRepo._map_to_domain(liability_model, liability_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[LiabilityDomain]:
        """Retrieve all liabilities of the account and return as a list of DomainObjects."""
        liability_model_list = db.session.scalars(
            sa.select(Liability).where(Liability.owner_id == account_id)
        ).all()
        return [
            LiabilityRepo._map_to_domain(liability, liability.owner.id)
            for liability in liability_model_list
        ]

    @staticmethod
    def delete_by_id(liability_id: int) -> None:
        """Given an liability ID, remove it from the database."""
        # Get liability_model from database
        liability_model = db.session.scalar(
            sa.select(Liability).where(Liability.id == liability_id)
        )
        if liability_model:
            db.session.delete(liability_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(liability_model: Liability, owner_id: str) -> LiabilityDomain:
        """Helper method to map the Liability model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return LiabilityDomain(
            id=liability_model.id,
            name=liability_model.name,
            principal_amount=liability_model.principal_amount,
            interest_rate=liability_model.interest_rate,
            start_age=liability_model.start_age,
            end_age=liability_model.end_age,
            created_at=liability_model.created_at,
            updated_at=liability_model.updated_at,
            description=liability_model.description,
            owner=owner_domain,
        )
