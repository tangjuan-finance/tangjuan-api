from app.domain.entities import ExpenseDomain
from app.repository.entities import ExpenseRepo
from .mixin import OwnerRequiredServiceMixin


class ExpenseService(OwnerRequiredServiceMixin):
    @staticmethod
    def create_expense(account_id: str, payload: dict) -> ExpenseDomain:
        """Create a new expense with validated owner."""
        owner = ExpenseService._get_owner(payload["owner_id"])
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

        return ExpenseRepo.get_by_id(expense_id)

    @staticmethod
    def get_expenses(account_id: str) -> list[ExpenseDomain]:
        """Retrieve all expenses for a given account."""
        return ExpenseRepo.get_list(account_id)

    @staticmethod
    def update_expense(account_id: str, payload: dict) -> ExpenseDomain:
        """Update an expense by ID if it exists."""
        expense_id = payload["id"]
        expense_from_repo = ExpenseRepo.get_by_id(expense_id)

        if not expense_from_repo:
            raise ValueError(f"Expense with ID {expense_id} not found")

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
        expense = ExpenseRepo.get_by_id(expense_id)

        if not expense:
            raise ValueError(f"Expense with ID {expense_id} not found")

        ExpenseRepo.delete_by_id(expense_id)
        return f"Expense {expense_id} deleted successfully"
