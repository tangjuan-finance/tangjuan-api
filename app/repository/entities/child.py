from app.domain.entities import ChildDomain
from app.infrastructure.models import Child, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class ChildRepo(EntityRepo):
    @staticmethod
    def create(child: ChildDomain) -> ChildDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        child_model = Child(
            name=child.name,
            birth_age=child.birth_age,
            child_saving_plan_id=child.child_saving_plan_id,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(child_model, attr, getattr(child, attr, None))

        parent = db.session.scalar(
            sa.select(Account).where(Account.id == child.parent.id)
        )
        if not parent:
            raise ValueError(f"Account with id {child.parent.id} not found")

        child_model.parent = parent

        # Save the Child model to the database
        db.session.add(child_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildRepo._map_to_domain(child_model, parent.id)

    @staticmethod
    def save(child: ChildDomain) -> ChildDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get child_model from database
        child_model = db.session.scalar(sa.select(Child).where(Child.id == child.id))
        if not child_model:
            raise ValueError("Child not found")

        parent = db.session.scalar(
            sa.select(Account).where(Account.id == child.parent.id)
        )
        if not parent:
            raise ValueError(f"Account with id {child.parent.id} not found")

        # Update Child Model
        child_model.name = child.name
        child_model.birth_age = child.birth_age
        child_model.child_saving_plan_id = child.child_saving_plan_id
        child_model.parent = parent

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(child_model, attr)
            setattr(child_model, attr, getattr(child, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ChildRepo._map_to_domain(child_model, parent.id)

    @staticmethod
    def get_by_id(child_id: int) -> ChildDomain | None:
        """Retrieve an child by ID and return as DomainObject."""
        # Get child_model from database
        child_model = db.session.scalar(sa.select(Child).where(Child.id == child_id))
        if not child_model:
            return None

        # Return the domain object with attributes populated from the database
        return ChildRepo._map_to_domain(child_model, child_model.parent.id)

    @staticmethod
    def get_list(account_id: str) -> list[ChildDomain]:
        """Retrieve all children of the account and return as a list of DomainObjects."""
        child_model_list = db.session.scalars(
            sa.select(Child).where(Child.parent_id == account_id)
        ).all()
        return [
            ChildRepo._map_to_domain(child, child.parent.id)
            for child in child_model_list
        ]

    @staticmethod
    def delete_by_id(child_id: int) -> None:
        """Given an child ID, remove it from the database."""
        # Get child_model from database
        child_model = db.session.scalar(sa.select(Child).where(Child.id == child_id))
        if child_model:
            db.session.delete(child_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(child_model: Child, parent_id: str) -> ChildDomain:
        """Helper method to map the Child model to a Domain Object."""
        parent_domain = AccountRepo.get_by_id(parent_id)
        return ChildDomain(
            id=child_model.id,
            name=child_model.name,
            birth_age=child_model.birth_age,
            created_at=child_model.created_at,
            updated_at=child_model.updated_at,
            description=child_model.description,
            child_saving_plan_id=child_model.child_saving_plan_id,
            parent=parent_domain,
        )
