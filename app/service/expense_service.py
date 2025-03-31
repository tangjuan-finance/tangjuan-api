from app.domain.entities import ExpenseDomain
from app.repository.entities import ExpenseRepo
from .mixin import OwnerRequiredServiceMixin


class ExpenseService(OwnerRequiredServiceMixin):
    @staticmethod
    def create_expense(account_id: str, payload: dict) -> ExpenseDomain:
        """Create a new expense with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authoirzed to create expense under the given owner"
            )

        # Get owner
        owner = ExpenseService._get_owner(owner_id)

        # Create the expense
        expense = ExpenseDomain(
            name=payload["name"],
            amount=payload["amount"],
            max_yearly_growth_rate=payload["max_yearly_growth_rate"],
            min_yearly_growth_rate=payload["min_yearly_growth_rate"],
            start_age=payload["start_age"],
            owner=owner,
        )
        return ExpenseRepo.create(expense)

    @staticmethod
    def get_expense_by_id(account_id: str, payload: dict) -> ExpenseDomain:
        """Retrieve a specific expense by ID."""
        expense_id = payload["id"]
        expense_from_repo = ExpenseRepo.get_by_id(expense_id)

        if not expense_from_repo:
            raise ValueError(f"Expense with ID {expense_id} not found")

        # Check if the account owns the expense
        if expense_from_repo.owner.id != account_id:
            raise PermissionError(f"Account {account_id} does not own this resource")

        return expense_from_repo

    @staticmethod
    def get_expenses(account_id: str) -> list[ExpenseDomain]:
        """Retrieve all expenses for a given account."""
        return ExpenseRepo.get_list(account_id)

    @staticmethod
    def update_expense(account_id: str, payload: dict) -> ExpenseDomain:
        """Update an expense by ID if it exists."""
        expense_from_repo = ExpenseService.get_expense_by_id(account_id, payload)

        params = {
            "name",
            "amount",
            "max_yearly_growth_rate",
            "min_yearly_growth_rate",
            "start_age",
        }

        for param in params:
            if param in payload:
                setattr(expense_from_repo, param, payload[param])

        return ExpenseRepo.save(expense_from_repo)

    @staticmethod
    def delete_expense_by_id(account_id: str, payload: dict) -> str:
        """Delete an expense by ID if it exists."""
        expense_id = payload["id"]

        try:
            ExpenseService.get_expense_by_id(account_id, payload)
        except ValueError as e:
            raise e
        except PermissionError as e:
            raise e

        ExpenseRepo.delete_by_id(expense_id)
        return f"Expense {expense_id} deleted successfully"
