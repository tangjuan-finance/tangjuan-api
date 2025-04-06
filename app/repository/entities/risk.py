from app.domain.entities import RiskDomain
from app.infrastructure.models import Risk, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class RiskRepo(EntityRepo):
    @staticmethod
    def create(risk: RiskDomain) -> RiskDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        risk_model = Risk(
            name=risk.name,
            max_loss=risk.max_loss,
            min_loss=risk.min_loss,
            start_age=risk.start_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description", "end_age"]
        for attr in optional_attributes:
            setattr(risk_model, attr, getattr(risk, attr, None))

        owner = db.session.scalar(sa.select(Account).where(Account.id == risk.owner.id))
        if not owner:
            raise ValueError(f"Account with id {risk.owner.id} not found")

        risk_model.owner = owner

        # Save the Risk model to the database
        db.session.add(risk_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return RiskRepo._map_to_domain(risk_model, owner.id)

    @staticmethod
    def save(risk: RiskDomain) -> RiskDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get risk_model from database
        risk_model = db.session.scalar(sa.select(Risk).where(Risk.id == risk.id))
        if not risk_model:
            raise ValueError("Risk not found")

        owner = db.session.scalar(sa.select(Account).where(Account.id == risk.owner.id))
        if not owner:
            raise ValueError(f"Account with id {risk.owner.id} not found")

        # Update Risk Model
        risk_model.name = risk.name
        risk_model.max_loss = risk.max_loss
        risk_model.min_loss = risk.min_loss
        risk_model.start_age = risk.start_age
        risk_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description", "end_age"]
        for attr in optional_attributes:
            origin_attr = getattr(risk_model, attr)
            setattr(risk_model, attr, getattr(risk, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return RiskRepo._map_to_domain(risk_model, owner.id)

    @staticmethod
    def get_by_id(risk_id: int) -> RiskDomain | None:
        """Retrieve an risk by ID and return as DomainObject."""
        # Get risk_model from database
        risk_model = db.session.scalar(sa.select(Risk).where(Risk.id == risk_id))
        if not risk_model:
            return None

        # Return the domain object with attributes populated from the database
        return RiskRepo._map_to_domain(risk_model, risk_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[RiskDomain]:
        """Retrieve all risks of the account and return as a list of DomainObjects."""
        risk_model_list = db.session.scalars(
            sa.select(Risk).where(Risk.owner_id == account_id)
        ).all()
        return [
            RiskRepo._map_to_domain(risk, risk.owner.id) for risk in risk_model_list
        ]

    @staticmethod
    def delete_by_id(risk_id: int) -> None:
        """Given an risk ID, remove it from the database."""
        # Get risk_model from database
        risk_model = db.session.scalar(sa.select(Risk).where(Risk.id == risk_id))
        if risk_model:
            db.session.delete(risk_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(risk_model: Risk, owner_id: str) -> RiskDomain:
        """Helper method to map the Risk model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return RiskDomain(
            id=risk_model.id,
            name=risk_model.name,
            max_loss=risk_model.max_loss,
            min_loss=risk_model.min_loss,
            start_age=risk_model.start_age,
            created_at=risk_model.created_at,
            updated_at=risk_model.updated_at,
            description=risk_model.description,
            end_age=risk_model.end_age,
            owner=owner_domain,
        )
