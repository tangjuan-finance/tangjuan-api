from app.domain.entities import ExpenseDomain
from app.repository.entities import ExpenseRepo
from .mixin import OwnerRequiredServiceMixin


class ExpenseService(OwnerRequiredServiceMixin):
    _required_fields = {
        "name",
        "amount",
        "max_yearly_growth_rate",
        "min_yearly_growth_rate",
        "start_age",
    }
    _all_fields = _required_fields | {
        "description",
        "end_age",
    }

    @staticmethod
    def create_expense(account_id: str, payload: dict) -> ExpenseDomain:
        """Create a new expense with validated owner."""

        owner_id = payload["owner_id"]

        # Check if account_id matches the owner_id
        if owner_id != account_id:
            raise PermissionError(
                f"Account {account_id} is not authorized to create expense under the given owner"
            )

        # Validate required fields
        missing_fields = ExpenseService._required_fields - payload.keys()
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Get owner
        owner = ExpenseService._get_owner(owner_id)

        # Filter payload to only include allowed fields
        expense_payload = {
            field: payload[field]
            for field in ExpenseService._all_fields
            if field in payload
        }
        expense_payload["owner"] = owner

        # Create the expense
        expense = ExpenseDomain(**expense_payload)
        return ExpenseRepo.create(expense)

    @staticmethod
    def get_expense_by_id(account_id: str, payload: dict) -> ExpenseDomain:
        """Retrieve a specific expense by ID."""
        expense_id = payload.get("id")
        if not expense_id:
            raise ValueError("Expense ID is required")
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

        for field in ExpenseService._all_fields:
            if field in payload:
                setattr(expense_from_repo, field, payload[field])

        return ExpenseRepo.save(expense_from_repo)

    @staticmethod
    def delete_expense_by_id(account_id: str, payload: dict) -> str:
        """Delete an expense by ID if it exists."""
        expense = ExpenseService.get_expense_by_id(
            account_id, payload
        )  # Raises if not found or unauthorized
        ExpenseRepo.delete_by_id(expense.id)
        return f"Expense {expense.id} deleted successfully"
