from app.domain.entities import ExpenseDomain
from app.infrastructure.models import Expense, Account
from app import db
import sqlalchemy as sa
from .account import AccountRepo
from .base import EntityRepo


class ExpenseRepo(EntityRepo):
    @staticmethod
    def create(expense: ExpenseDomain) -> ExpenseDomain:
        """Given a DomainObject, store it in the database and return the stored object."""
        # Instance with required attr
        expense_model = Expense(
            id=expense.id,
            name=expense.name,
            amount=expense.amount,
            max_yearly_growth_rate=expense.max_yearly_growth_rate,
            min_yearly_growth_rate=expense.min_yearly_growth_rate,
            start_age=expense.start_age,
            end_age=expense.end_age,
        )

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            setattr(expense_model, attr, getattr(expense, attr, None))

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == expense.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {expense.owner.id} not found")

        expense_model.owner = owner

        # Save the Expense model to the database
        db.session.add(expense_model)
        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ExpenseRepo._map_to_domain(expense_model, owner.id)

    @staticmethod
    def save(expense: ExpenseDomain) -> ExpenseDomain:
        """Given an existing DomainObject, update it in the database and return the updated object."""
        # Get expense_model from database
        expense_model = db.session.scalar(
            sa.select(Expense).where(Expense.id == expense.id)
        )
        if not expense_model:
            raise ValueError("Expense not found")

        owner = db.session.scalar(
            sa.select(Account).where(Account.id == expense.owner.id)
        )
        if not owner:
            raise ValueError(f"Account with id {expense.owner.id} not found")

        # Update Expense Model
        expense_model.name = expense.name
        expense_model.amount = expense.amount
        expense_model.max_yearly_growth_rate = expense.max_yearly_growth_rate
        expense_model.min_yearly_growth_rate = expense.min_yearly_growth_rate
        expense_model.start_age = expense.start_age
        expense_model.end_age = expense.end_age
        expense_model.owner = owner

        # Set optional attributes if present in the domain object
        optional_attributes = ["description"]
        for attr in optional_attributes:
            origin_attr = getattr(expense_model, attr)
            setattr(expense_model, attr, getattr(expense, attr, origin_attr))

        db.session.commit()

        # Return the domain object with attributes populated from the database
        return ExpenseRepo._map_to_domain(expense_model, owner.id)

    @staticmethod
    def get_by_id(expense_id: int) -> ExpenseDomain | None:
        """Retrieve an expense by ID and return as DomainObject."""
        # Get expense_model from database
        expense_model = db.session.scalar(
            sa.select(Expense).where(Expense.id == expense_id)
        )
        if not expense_model:
            return None

        # Return the domain object with attributes populated from the database
        return ExpenseRepo._map_to_domain(expense_model, expense_model.owner.id)

    @staticmethod
    def get_list(account_id: str) -> list[ExpenseDomain]:
        """Retrieve all expenses of the account and return as a list of DomainObjects."""
        expense_model_list = db.session.scalars(
            sa.select(Expense).where(Expense.owner_id == account_id)
        ).all()
        return [
            ExpenseRepo._map_to_domain(exp, exp.owner.id) for exp in expense_model_list
        ]

    @staticmethod
    def delete_by_id(expense_id: int) -> None:
        """Given an expense ID, remove it from the database."""
        # Get expense_model from database
        expense_model = db.session.scalar(
            sa.select(Expense).where(Expense.id == expense_id)
        )
        if expense_model:
            db.session.delete(expense_model)
            db.session.commit()

        return None

    @staticmethod
    def _map_to_domain(expense_model: Expense, owner_id: str) -> ExpenseDomain:
        """Helper method to map the Expense model to a Domain Object."""
        owner_domain = AccountRepo.get_by_id(owner_id)
        return ExpenseDomain(
            _id=expense_model.id,
            name=expense_model.name,
            amount=expense_model.amount,
            max_yearly_growth_rate=expense_model.max_yearly_growth_rate,
            min_yearly_growth_rate=expense_model.min_yearly_growth_rate,
            start_age=expense_model.start_age,
            created_at=expense_model.created_at,
            updated_at=expense_model.updated_at,
            description=expense_model.description,
            end_age=expense_model.end_age,
            owner=owner_domain,
        )
