from app.domain.entities import IncomeDomain
from app.infrastructure.models import Income, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class IncomeRepo(EntityRepo):
    @staticmethod
    def create(income: IncomeDomain) -> IncomeDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        income_model = Income(
            name=income.name,
            amount=income.amount,
            max_yearly_growth_rate=income.max_yearly_growth_rate,
            min_yearly_growth_rate=income.min_yearly_growth_rate,
            start_age=income.start_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description", "end_age"]
        for attr in optional_attributes:
            setattr(income_model, attr, getattr(income, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == income.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {income.owner.id} not found")

        income_model.owner = owner

        # Save the Income model to the database
        db.session.add(income_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return IncomeRepo._map_to_domain(income_model, owner.id)

    @staticmethod
    def save(income: IncomeDomain) -> IncomeDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get income_model from database
        income_model = db.session.scalar(
            sa.select(Income).where(Income.id == income.id)
        )
        if not income_model:
            raise ValueError("Income not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == income.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {income.owner.id} not found")

        # Update Income Model
        income_model.name = income.name
        income_model.amount = income.amount
        income_model.max_yearly_growth_rate = income.max_yearly_growth_rate
        income_model.min_yearly_growth_rate = income.min_yearly_growth_rate
        income_model.start_age = income.start_age
        income_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description", "end_age"]
        for attr in optional_attributes:
            origin_attr = getattr(income_model, attr)
            setattr(income_model, attr, getattr(income, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return IncomeRepo._map_to_domain(income_model, owner.id)

    @staticmethod
    def get_by_id(income_id: int) -> IncomeDomain | None:
        """Retrieve an income by ID and return as DomainObject."""
        # Get income_model from database
        income_model = db.session.scalar(
            sa.select(Income).where(Income.id == income_id)
        )
        if not income_model:
            return None

        # Return the domain object with attributes populated from the database
        return IncomeRepo._map_to_domain(income_model, income_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[IncomeDomain]:
        """Retrieve all incomes of the account and return as a list of DomainObjects."""
        income_model_list = db.session.scalars(
            sa.select(Income).where(Income.owner_id == account_id)
        ).all()
        return [
            IncomeRepo._map_to_domain(income, income.owner.id)
            for income in income_model_list
        ]

    @staticmethod
    def delete_by_id(income_id: int) -> None:
        """Given an income ID, remove it from the database."""
        # Get income_model from database
        income_model = db.session.scalar(
            sa.select(Income).where(Income.id == income_id)
        )
        if income_model:
            db.session.delete(income_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(income_model: Income, owner_id: str) -> IncomeDomain:
        """Helper method to map the Income model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return IncomeDomain(
            id=income_model.id,
            name=income_model.name,
            amount=income_model.amount,
            max_yearly_growth_rate=income_model.max_yearly_growth_rate,
            min_yearly_growth_rate=income_model.min_yearly_growth_rate,
            start_age=income_model.start_age,
            created_at=income_model.created_at,
            updated_at=income_model.updated_at,
            description=income_model.description,
            end_age=income_model.end_age,
            owner=owner_domain,
        )
